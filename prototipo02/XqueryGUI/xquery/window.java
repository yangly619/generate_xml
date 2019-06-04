import java.awt.Color;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

import javax.swing.*;


public class window extends JFrame {
	
	private JSplitPane splitpanel;
	private JPanel panel_top;
	private JScrollPane panel_down;
	private JComboBox<String>  query_examples;
	private JLabel label;
	private JTextArea text_query;
	private JCheckBox check;
	private JButton button;
	private String fileString = "xquery/bd_xml.xml";
	private String query= null;
	private xqueryTest xquery = new xqueryTest();
	private File f1;
	private JTextArea resultArea;
	public window() {
		
		splitpanel = new JSplitPane(JSplitPane.VERTICAL_SPLIT);
		this.setContentPane(splitpanel);
		panel_top = new JPanel();
		panel_top.setLayout(null);
		panel_down = new JScrollPane();
		panel_top.setBorder(BorderFactory.createLineBorder(Color.orange));
		panel_down.setBorder(BorderFactory.createLineBorder(Color.orange));
		splitpanel.setDividerSize(5);
		splitpanel.setDividerLocation(250);
		splitpanel.setLeftComponent(panel_top);
		splitpanel.setRightComponent(panel_down);
		label = new JLabel("ExistDB xquery");
		label.setBounds(250,0,100,50);
		panel_top.add(label);
		query_examples = new JComboBox<String>();
		query_examples.setBounds(100,40,400,50);
		query_examples.addItem("Mostrar los genes que codifican la enfermedad \"enf_45FB9D9\":");
		query_examples.addItem("Mostrar los pacientes femeninas que padece la enfermedad \"enf_2B0EA74\" y los tratamientos:");
		query_examples.addItem("Mostrar una lista de pacientes y sus fechas de ingreso que padece la enfermeda \"enf_45FB9D9\":");
		
		panel_top.add(query_examples);
		check = new JCheckBox("Nueva consulta");
		check.setBounds(100,70,150,50);
		panel_top.add(check);
		text_query = new JTextArea("for $s in /pacientes\n" + 
				"return $s");
		text_query.setBounds(105,120,380,110);
		panel_top.add(text_query);
		resultArea = new JTextArea();
		panel_down.add(resultArea);
		
		button = new JButton("Start");
		button.setBounds(500,200,60,30);
		button.addActionListener(new ActionListener() {

			@Override
			public void actionPerformed(ActionEvent arg0) {
				if(!check.isSelected()) {
					if(query_examples.getSelectedIndex()==0)
						query = "for $enfermedad in /pacientes/paciente/enfermedad\n" + 
								"where $enfermedad/IdENFERM = \"enf_45FB9D9\"\n" + 
								"return ($enfermedad/GEN/idGEN,$enfermedad/GEN/NOMBRE,$enfermedad/GEN/LOCALIZAICION)";
					 else if (query_examples.getSelectedIndex()==1)
						 query = "for $paciente in /pacientes/paciente\n" + 
						 		"where $paciente/enfermedad/IdENFERM =\"enf_2B0EA74\" and $paciente/SEXO = \"F\"\n" + 
						 		"return ($paciente/DNI,$paciente/enfermedad/tratamiento/idTRATAMIENTO,$paciente/enfermedad/tratamiento/NOMBRE)";
					 else if (query_examples.getSelectedIndex()==2)
						 query = "for $paciente in /pacientes/paciente\n" + 
						 		"where $paciente/enfermedad/IdENFERM =\"enf_45FB9D9\"\n" + 
						 		"return ($paciente/DNI,$paciente/FECHA_INGRESO)";
					//xquery.select(fileString,query);
				}
				else if (check.isSelected()) {
					query = text_query.getText().toString();
				}
				xquery.select(fileString,query);
				
				f1 = new File("/Users/yangyangli/Desktop/Ingenieria/bdBiologico/generaXML/prototipo02/XqueryGUI/result.xml");   
				JFileChooser fileChooser = new JFileChooser();	 
				fileChooser.setSelectedFile(f1);
				fileChooser.showSaveDialog(null);

			}
			
		} );
		
		panel_top.add(button);

		this.setSize(600, 600);
		this.setTitle("Xquery");
		this.setVisible(true);
		this.setLocationRelativeTo(null);
		this.setDefaultCloseOperation(EXIT_ON_CLOSE);
	}
	
	
	
	

}
