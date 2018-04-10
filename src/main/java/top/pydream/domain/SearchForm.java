package top.pydream.domain;

import org.hibernate.validator.constraints.NotBlank;

public class SearchForm {

    @NotBlank(message = "微信号选择不能为空!")
    String wechat;

    public String getKeyword() {
        return keyword;
    }

    public void setKeyword(String keyword) {
        this.keyword = keyword;
    }

    @NotBlank(message = "搜索关键词不能为空!")
    String keyword;

    public String getWechat() {
        return wechat;
    }

    public void setWechat(String wechat) {
        this.wechat = wechat;
    }
}
