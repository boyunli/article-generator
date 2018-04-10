package top.pydream.domain;

import java.io.Serializable;

public class Account implements Serializable{

    private static final long serialVersionUID = 1L;
    private Long id;
    private String wechat;
    private String desc;

    public String getWechat() {
        return wechat;
    }

    public void setWechat(String wechat) {
        this.wechat = wechat;
    }

    public String getDesc() {
        return desc;
    }

    public void setDesc(String desc) {
        this.desc = desc;
    }
}
