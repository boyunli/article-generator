package top.pydream.domain;

import org.hibernate.validator.constraints.NotBlank;

public class SearchForm {

    @NotBlank(message = "搜索关键词不能为空!")
    String keyword;

    @NotBlank(message = "搜索类别不能为空!")
    String category;

    @NotBlank(message = "微信号选择不能为空!")
    String wechat;

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }

    public String getWechat() {
        return wechat;
    }

    public void setWechat(String wechat) {
        this.wechat = wechat;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }
}
