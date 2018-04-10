package top.pydream.domain;

import java.util.List;

public class AjaxResponseBody {

    String msg;
    List<PseudoNews> result;

    public String getMsg() {
        return msg;
    }

    public void setMsg(String msg) {
        this.msg = msg;
    }

    public List<PseudoNews> getResult() {
        return result;
    }

    public void setResult(List<PseudoNews> result) {
        this.result = result;
    }
}
