package top.pydream.generator.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import top.pydream.generator.domain.News;
import top.pydream.generator.service.NewsService;
import top.pydream.generator.utils.Synonyms;

import java.util.List;

@RestController
public class EsController {

    @Autowired
    private NewsService newsService;

    @RequestMapping(value = "/api/news/tag/find", method = RequestMethod.GET)
    public List<News> queryArticleByTag(@RequestParam(value = "tag") String tag) {
        List<News> news = newsService.findByTag(tag);
        return news;
    }

    @RequestMapping(value = "/api/news/like/find", method = RequestMethod.GET)
    public String findBySecondLike(@RequestParam(value = "keyword") String keyword) {
        List<News> news = newsService.findBySecondLike(keyword);
        List<News> subNews = news.subList(0, 1);
        String replaceNew = "";
        for (News anew: subNews) {
            replaceNew = Synonyms.synonymsReplacement(anew.getSecond(), 0.6);
        }
        return replaceNew;
    }



}
