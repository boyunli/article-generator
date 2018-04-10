package top.pydream.web;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindingResult;
import org.springframework.validation.Errors;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.ModelAndView;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;
import top.pydream.domain.AjaxResponseBody;
import top.pydream.domain.News;
import top.pydream.domain.PseudoNews;
import top.pydream.domain.SearchForm;
import top.pydream.domain.Account;
import top.pydream.service.AccountService;
import top.pydream.service.NewsService;
import top.pydream.utils.Synonyms;

import javax.validation.Valid;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@RestController
public class EsController {

    @Autowired
    private NewsService newsService;

    @Autowired
    private AccountService accountService;

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


    @PostMapping("/search")
    public ResponseEntity<?> createPseudo(@Valid @RequestBody SearchForm searchForm, Errors errors) {

        AjaxResponseBody result = new AjaxResponseBody();

        if (errors.hasErrors()) {
            result.setMsg(errors.getAllErrors()
                    .stream().map(x -> x.getDefaultMessage())
                    .collect(Collectors.joining(",")));
            return ResponseEntity.badRequest().body(result);
        }

        Account account = accountService.findByWeixin(searchForm.getWechat());
        String keyword = searchForm.getKeyword();
        List<News> news = newsService.findBySecondLike(keyword);
        List<News> subNews = news.subList(0, 3);
        List<PseudoNews> pseudoNews = new ArrayList<PseudoNews>();
        for (News anew: subNews) {
            String replaceNew = Synonyms.synonymsReplacement(anew.getSecond(), 0.6);
            String union = keyword + "。" + account.getDesc() + "<br/>"
                    + replaceNew + keyword + "<br/>"
                    + "以上就是" + keyword + "全部介绍，感兴趣的小伙伴赶快来资讯我们吧，谢谢阅读。";
            pseudoNews.add(new PseudoNews(anew.getTitle(), anew.getTag(), union));
        }
        if (pseudoNews.isEmpty()) {
            result.setMsg("没有符合 " + keyword + " 的伪原创， 请换一个关键词试试!");
        } else {
            result.setMsg("success");
        }
        result.setResult(pseudoNews);
        return ResponseEntity.ok(result);
    }
}