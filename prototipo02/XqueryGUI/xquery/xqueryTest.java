import java.io.File;
import java.io.IOException;
import java.util.Properties;
 
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.ParserConfigurationException;
import javax.xml.transform.OutputKeys;
import javax.xml.transform.stream.StreamResult;
 
import org.w3c.dom.Document;
import org.xml.sax.SAXException;
 
import net.sf.saxon.Configuration;
import net.sf.saxon.dom.*;
import net.sf.saxon.query.DynamicQueryContext;
import net.sf.saxon.query.StaticQueryContext;
import net.sf.saxon.query.XQueryExpression;
import net.sf.saxon.trans.XPathException;
public class xqueryTest {
	public static void select(String fileString ,String query ){
		
		  //document object
		  Document document = getDocument(fileString);
		  Configuration configuration = new Configuration();
		  StaticQueryContext context = new StaticQueryContext(configuration, false);
		  //query
		  XQueryExpression expression = null;
		  try {
		   expression = context.compileQuery(query);
		   DynamicQueryContext context2 = new DynamicQueryContext(configuration);
		   context2.setContextItem(new DocumentWrapper(document,null,configuration));
		   
		   final Properties props = new Properties();
		            props.setProperty(OutputKeys.METHOD, "xml");
		            props.setProperty(OutputKeys.INDENT, "yes");
		            //run and show result
		            File f = new File("result.xml");
		            expression.run(context2, new StreamResult(f), props);
		
		            
		  } catch (XPathException e) {
		   // TODO Auto-generated catch block
		   e.printStackTrace();
		  }
		  
		 }
		 
		 public static Document getDocument(String xml){
		  DocumentBuilderFactory builderFactory = DocumentBuilderFactory.newInstance();
		  DocumentBuilder builder;
		  Document document = null;
		  try {
		   builder = builderFactory.newDocumentBuilder();
		   document = builder.parse(xml);
		  } catch (ParserConfigurationException e) {
		   // TODO Auto-generated catch block
		   e.printStackTrace();
		  } catch (SAXException e) {
		   // TODO Auto-generated catch block
		   e.printStackTrace();
		  } catch (IOException e) {
		   // TODO Auto-generated catch block
		   e.printStackTrace();
		  }
		  document.normalize();
		  return document;
		 }
		
}
