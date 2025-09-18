
import net.sf.json.JSONObject;

import java.io.*;
import java.net.MalformedURLException;
import java.util.ArrayList;

import java.net.URL;
import java.net.URLConnection;



/**
 * Created by xingweidong on 2018/6/11.
 */
public class JsonDemo {
    /**
     * 以行为单位读取文件，常用于读面向行的格式化文件
     * @param fileName ids.txt文件的绝对路径
     * @return 数组类型的ids
     */
    public static ArrayList readFileByLines(String fileName) {
        File file = new File(fileName);
        BufferedReader reader = null;
        ArrayList ids = new ArrayList();
        try {
            System.out.println("以行为单位读取文件内容，一次读一整行：");
            reader = new BufferedReader(new FileReader(file));
            String tempString = null;

            // 一次读入一行，直到读入null为文件结束
            while ((tempString = reader.readLine()) != null) {
                // 将读取的每一行处理后得到的有效内容作为数组元素加入到数组ids中
                ids.add(tempString.split("\\s")[2]);
            }
            reader.close();
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            if (reader != null) {
                try {
                    reader.close();
                } catch (IOException e1) {
                }
            }
        }
        return ids;
    }


    /**
     * 获取区块链json
     * @param bcurl 区块链访问url
     * @return 可处理的区块链json信息
     */
    public static String loadJSON(String bcurl) {
        StringBuilder json = new StringBuilder();
        try {
            URL url = new URL(bcurl);
            URLConnection yc = url.openConnection();
            BufferedReader in = new BufferedReader(new InputStreamReader(
                    yc.getInputStream(),"utf-8"));//防止乱码
            String inputLine = null;
            while ((inputLine = in.readLine()) != null) {
                    json.append(inputLine);
            }
            // 去除第一个 [  和最后一个 ]
            json.delete(0,1);
            json.deleteCharAt(json.length()-1);

            in.close();
        } catch (MalformedURLException e) {
        } catch (IOException e) {
        }

        return json.toString();
    }


    /**
     * 处理获取到的区块链json
     * @param ids 处理ids.txt文件得到的区块链id数组
     * @param bcurl 区块链访问url
     * @param idIndex 区块链id数组ids的索引
     * @return 处理区块链json后，得到的新的json
     */
    public static JSONObject handleJson(ArrayList ids, String bcurl, String idIndex) {

        String json = loadJSON(bcurl);
        //System.out.println(json);

        // 字符串转json
        JSONObject jsonObj = JSONObject.fromObject(json);
        String asset = jsonObj.getString("asset");
        JSONObject jsonObj2 = JSONObject.fromObject(asset);
        String data = jsonObj2.getString("data");
        JSONObject jsonObj3 = JSONObject.fromObject(data);
        jsonObj3.put("id", ids.get(Integer.parseInt(idIndex)));
        jsonObj2.put("tea", jsonObj3);
        jsonObj2.remove("data");

        return jsonObj2;

    }


    public static void main(String[] args){
        // 读取保存区块链id的文件ids.txt，得到一个ArraryList
        File file = new File("../data/ids.txt");
        String fileName = file.getAbsolutePath();

        // 生成ids
        ArrayList ids = readFileByLines(fileName);

        // 代表传入的查询idIndex
        String idIndex = String.valueOf(0);

        // http://192.168.0.121:9984/api/v1/transactions?asset_id=64c6f2c1a68fb8810d5598ae67eb1345fadd226f6ccc1fb17cf98bf032413e7d
        String bcurl = "http://api.xingliannong.com/api/v1/transactions?asset_id=" + ids.get(Integer.parseInt(idIndex));

        // 得到目标json
        JSONObject jsonObject = handleJson(ids, bcurl, idIndex);

        // 打印
        System.out.println(jsonObject);
    }


}
