package top.pydream.utils;

import java.util.ArrayList;
import java.util.Hashtable;
import java.util.List;
import java.util.Iterator;
import java.util.Random;
import java.io.File;
import com.hankcs.hanlp.HanLP;
import com.hankcs.hanlp.seg.common.Term;

public class Synonyms {
	private static Hashtable<String, String> hashtable = new Hashtable<String, String>();
	
	private static void init() {
		if ((new File("/home/lily/jwork/hashtable.ser")).exists())
			Synonyms.hashtable = (new SerializableHashtable()).load("/home/lily/jwork/hashtable.ser").get();
		else {
			ExcelOperator operator = new ExcelOperator("d:/idea_workspace/00/article-generator/src/main/java/top/pydream/utils/synonyms.xls");
//			ExcelOperator operator = new ExcelOperator("/home/lily/jwork/synonyms.xls");
			ArrayList<String[]> pairs = new ArrayList<String[]>();
			pairs.addAll(operator.getPairs(0, 0, 1));
			pairs.addAll(operator.getPairs(0, 3, 1));
			pairs.addAll(operator.getPairs(0, 6, 1));
			operator.close();
			
			SerializableHashtable serializableHashtable = new SerializableHashtable(pairs);
//			serializableHashtable.store("d:/idea_workspace/00/article-generator/src/main/java/top/pydream/utils/hashtable.ser");
			serializableHashtable.store("/home/lily/jwork/hashtable.ser");
			Synonyms.hashtable = serializableHashtable.get();
		}
	}
	
	private static String getSynonym(String origin) {
		if (Synonyms.hashtable.containsKey(origin)) return Synonyms.hashtable.get(origin);
		return origin;
	}
	
	public static String synonymsReplacement(String origin, double threshold) {
		init();
		if (threshold > 1.0d) return origin;
		if (threshold < 0.0d) threshold = 0.0d;
		
		List<Term> termsList = HanLP.segment(origin);
		String out = "";
		for (Iterator<Term> termsIterator = termsList.iterator(); termsIterator.hasNext();) {
			 Term term = termsIterator.next();
			 String word = ((new Random()).nextDouble() >= threshold) ? Synonyms.getSynonym(term.word) : term.word;
			 out += word;
		}
		return out;
	}
	
//	public static void main(String[] args) {
//		Synonyms.init();
//		System.out.println(Synonyms.synonymsReplacement(args[0], 0.6));
//	}
}
