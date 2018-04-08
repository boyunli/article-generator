package top.pydream.generator.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import top.pydream.generator.domain.News;
import top.pydream.generator.service.NewsService;

import java.util.List;

@RestController
public class EsController {

    @Autowired
    private NewsService newsService;

    @RequestMapping(value = "/api/news/tag/find", method = RequestMethod.GET)
    public List<News> queryArticleByTag(@RequestParam(value = "tag") String tag) {
        return newsService.findByTag(tag);
    }

    @RequestMapping(value = "/api/news/like/find", method = RequestMethod.GET)
    public List<News> findBySecondLike(@RequestParam(value = "second") String second) {
        return newsService.findBySecondLike(second);
    }

}
