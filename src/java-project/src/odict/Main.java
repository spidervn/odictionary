package odict;

import java.io.IOException;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;

import com.sun.xml.internal.ws.developer.MemberSubmissionEndpointReference.Elements;

public class Main {

	protected static void testJsoup() {
		String url = "https://en.oxforddictionaries.com/definition/intuitively";
		try {
			Document doc = Jsoup.connect(url).get();
			System.out.println(doc.title());
			
			org.jsoup.select.Elements els = doc.getElementsByClass("pos");
			for (Element link : els) {
				System.out.println(link.ownText());
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public static void main(String[] args) {
		testJsoup();
	}
}
