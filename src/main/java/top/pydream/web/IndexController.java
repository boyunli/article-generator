package top.pydream.web;

import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.servlet.ModelAndView;
import top.pydream.domain.News;

@Controller
public class IndexController {

    @GetMapping("/")
    public String index() {
        return "index";
    }

//    @GetMapping
//    public ModelAndView index() {
//        Iterable<News> news = null;
//        return new ModelAndView("index", "news", news);
//    }
}
