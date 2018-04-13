package top.pydream.service;

import top.pydream.domain.News;

import java.util.List;

public interface NewsService {

    List<News> searchSecond(Integer pageNumber, Integer pageSize, String second);
}
