package odict.app.Interface;

import java.util.ArrayList;

public class AMeaning {
	String meaning;
	ArrayList<String> examples;
	ArrayList<ASubMeaning> subMeaning;
	
	public AMeaning() {
		examples = new ArrayList<String>();
		subMeaning = new ArrayList<ASubMeaning>();
	}
	
	
}
