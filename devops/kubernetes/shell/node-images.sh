#!/usr/bin/env bash

set -u

DEFAULT_NODES_FILE="./nodes"
NODES_FILE="$DEFAULT_NODES_FILE"
SINGLE_NODE=""
COMMAND=""
IMAGE_REFS=()
SKIP_CONFIRM=false

usage() {
    cat <<'EOF'
Usage:
  scripts/k8s-node-images.sh [--nodes-file PATH] list
  scripts/k8s-node-images.sh [--nodes-file PATH] [--yes] remove <image-or-id>...
  scripts/k8s-node-images.sh --node <ssh-target> list
  scripts/k8s-node-images.sh --node <ssh-target> [--yes] remove <image-or-id>...

Options:
  --nodes-file PATH  Read SSH targets from PATH instead of ./nodes.
  --node NODE        Operate on one SSH target instead of reading a node file.
  --yes              Skip confirmation prompt for remove.
  -h, --help         Show this help message.
EOF
}

fail_usage() {
    echo "Error: $1" >&2
    echo >&2
    usage >&2
    exit 2
}

parse_args() {
    local args=()
    while (($# > 0)); do
        case "$1" in
            --nodes-file)
                (($# >= 2)) || fail_usage "--nodes-file requires a path"
                NODES_FILE="$2"
                shift 2
                ;;
            --node)
                (($# >= 2)) || fail_usage "--node requires an SSH target"
                SINGLE_NODE="$2"
                shift 2
                ;;
            --yes)
                SKIP_CONFIRM=true
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            list|remove)
                if [[ -n "$COMMAND" ]]; then
                    fail_usage "duplicate command: $1"
                fi
                COMMAND="$1"
                shift
                ;;
            *)
                if [[ -z "$COMMAND" ]]; then
                    fail_usage "unknown argument: $1"
                else
                    args+=("$1")
                    shift
                fi
                ;;
        esac
    done

    [[ -n "$COMMAND" ]] || fail_usage "command is required"

    case "$COMMAND" in
        list)
            ((${#args[@]} == 0)) || fail_usage "list does not accept extra arguments"
            ;;
        remove)
            ((${#args[@]} >= 1)) || fail_usage "remove requires at least one image name or ID"
            IMAGE_REFS=("${args[@]}")
            ;;
    esac
}

get_nodes() {
    if [[ -n "$SINGLE_NODE" ]]; then
        echo "$SINGLE_NODE"
        return
    fi

    if [[ ! -f "$NODES_FILE" ]]; then
        echo "Error: nodes file not found: $NODES_FILE" >&2
        exit 1
    fi

    grep -v '^\s*#' "$NODES_FILE" | grep -v '^\s*$' || true
}

run_on_node() {
    local node="$1"
    shift
    ssh -n -o ConnectTimeout=10 -o StrictHostKeyChecking=accept-new "$node" "$@"
}

cmd_list() {
    local node
    while IFS= read -r node; do
        echo "========== $node =========="
        if run_on_node "$node" "crictl images" 2>/dev/null | awk 'NR==1 { print "IMAGE:TAG"; next } /^10\.111\.119\.190:30002/ { print $1":"$2 }'; then
            :
        else
            echo "Failed to list images on $node" >&2
        fi
        echo
    done
}

cmd_remove() {
    local node image_ref
    local failed_nodes=()

    if ! $SKIP_CONFIRM; then
        echo
        echo "========================================"
        echo "  DELETE CONFIRMATION REQUIRED"
        echo "========================================"
        echo
        echo "Images to remove:"
        for image_ref in "${IMAGE_REFS[@]}"; do
            echo "  - $image_ref"
        done
        echo
        echo "Target nodes:"
        while IFS= read -r node; do
            echo "  - $node"
        done
        echo
        read -rp "Type 'y' to confirm deletion, or any other key to cancel: " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            echo
            echo "Operation cancelled. No images were removed."
            echo "Tip: Use --yes to skip this confirmation."
            exit 0
        fi
    fi

    while IFS= read -r node; do
        for image_ref in "${IMAGE_REFS[@]}"; do
            echo "==> Removing '$image_ref' from $node ..."

            local output rc
            output=$(run_on_node "$node" "crictl rmi '$image_ref'" 2>&1)
            rc=$?

            if ((rc == 0)); then
                echo "    Done."
            elif echo "$output" | grep -qiE 'not found|not known|no such image|image not known|does not exist'; then
                echo "    Not found, skipped."
            else
                echo "    Failed."
                failed_nodes+=("$node")
            fi
        done
    done

    if ((${#failed_nodes[@]} > 0)); then
        echo
        echo "Remove failed on the following nodes:"
        printf '  - %s\n' "${failed_nodes[@]}"
        exit 1
    fi

    echo
    echo "All specified images removed successfully from all nodes."
}

main() {
    parse_args "$@"

    case "$COMMAND" in
        list)
            get_nodes | cmd_list
            ;;
        remove)
            get_nodes | cmd_remove
            ;;
    esac
}

main "$@"
