package top.pydream;

import org.mybatis.spring.annotation.MapperScan;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@MapperScan("top.pydream.dao")
@SpringBootApplication
public class ArticleGeneratorApplication {

	public static void main(String[] args) {
		SpringApplication.run(ArticleGeneratorApplication.class, args);
	}
}
