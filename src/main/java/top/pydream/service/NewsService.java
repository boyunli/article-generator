package top.pydream.service;

import top.pydream.domain.News;

import java.util.List;

public interface NewsService {

    List<News> searchContent(Integer pageNumber, Integer pageSize, String content);
}
