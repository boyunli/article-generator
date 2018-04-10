package top.pydream.domain;

public class PseudoNews {

    private String title;
    private String tag;

    public PseudoNews(String title, String tag, String content) {
        this.title = title;
        this.tag = tag;
        this.content = content;
    }

    private String content;

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getTag() {
        return tag;
    }

    public void setTag(String tag) {
        this.tag = tag;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

}
