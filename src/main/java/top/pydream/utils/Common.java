package top.pydream.utils;

import top.pydream.domain.News;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class Common {

    public static <T> List<T> randomSubList(List<T> list, int newSize) {
        list = new ArrayList<>(list);
        Collections.shuffle(list);
        return list.subList(0, newSize);
    }

    public static List<String> divideParas(List<News> news) {
        List<String> paragraphs = new ArrayList<>();
        for (News anew : news) {
            String[] contents = anew.getContent().split("&&&");
            for (String content: contents) {
                if (content.length() < 20) {
                    continue;
                } else  {
                    paragraphs.add(content);
                }
            }
        }
        return paragraphs;
    }

    /**
     * 随机指定范围内N个不重复的数
     * 最简单最基本的方法
     * @param min 指定范围最小值
     * @param max 指定范围最大值
     * @param n 随机数个数
     */
    public static int[] randomPara(int min, int max, int n){
        if (n > (max - min + 1) || max < min) {
            return null;
        }
        int[] result = new int[n];
        int count = 0;
        while(count < n) {
            int num = (int) (Math.random() * (max - min)) + min;
            boolean flag = true;
            for (int j = 0; j < n; j++) {
                if(num == result[j]){
                    flag = false;
                    break;
                }
            }
            if(flag){
                result[count] = num;
                count++;
            }
        }
        return result;
    }
}
