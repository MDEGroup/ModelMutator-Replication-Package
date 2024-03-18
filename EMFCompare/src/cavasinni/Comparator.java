package cavasinni;

import java.util.ArrayList;
import java.util.List;

import org.eclipse.emf.ecore.util.BasicExtendedMetaData;
import org.eclipse.emf.ecore.util.ExtendedMetaData;
import org.eclipse.emf.common.util.URI;
import org.eclipse.emf.compare.Comparison;
import org.eclipse.emf.compare.EMFCompare;
import org.eclipse.emf.compare.Match;
import org.eclipse.emf.compare.scope.DefaultComparisonScope;
import org.eclipse.emf.compare.scope.IComparisonScope;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.resource.Resource;
import org.eclipse.emf.ecore.resource.ResourceSet;
import org.eclipse.emf.ecore.resource.impl.ResourceSetImpl;
import org.eclipse.emf.ecore.xmi.XMLResource;
import org.eclipse.emf.ecore.xmi.impl.EcoreResourceFactoryImpl;
import org.eclipse.emf.ecore.xmi.impl.XMIResourceFactoryImpl;
import org.eclipse.uml2.uml.UMLPackage;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.regex.Pattern;
import java.util.stream.Stream;

public class Comparator {

	/*
	 * public static void main (String[] args) {
	 * 
	 * String ecoreMM = "GPTMutators/RQ2/Families2Persons/Families.ecore"; String
	 * mutatedOriginal = "GPTMutators/RQ2/Families2Persons/Output0.model";
	 * 
	 * String gptMutated =
	 * "GPTMutators/RQ2/Families2Persons/families_mutants_run_10/corrected_mutant_1.xml";
	 * 
	 * System.out.println(calculateSimilarity2(ecoreMM, mutatedOriginal,
	 * gptMutated));
	 * 
	 * }
	 */

	public static void main(String[] args) {
	     String basePath = "GPTMutators/RQ1/pfsm/";
	        String ecoreMM = basePath + "PFSM.ecore";
	        String mutatedOriginal = basePath + "Output0.model";

	        try {
	            Files.walk(Paths.get(basePath))
	                .filter(Files::isDirectory)
	                .forEach(folder -> {
	                    String folderName = folder.getFileName().toString();
	                    if (Pattern.matches("pfsm_mutants_run_\\d+", folderName)) {
	                        processFolder(folder, ecoreMM, mutatedOriginal);
	                    }
	                });
	        } catch (IOException e) {
	            System.err.println("An error occurred during initial directory walk");
	            //e.printStackTrace();
	        }
	}

	private static void processFolder(Path folder, String ecoreMM, String mutatedOriginal) {
		try (Stream<Path> files = Files.walk(folder)) {
			files.filter(file -> file.toString().endsWith(".xml")).forEach(file -> {
				try {
					String gptMutated = file.toString();
					System.out.println("Comparing: " + mutatedOriginal + " with " + gptMutated);
					System.out.println(calculateSimilarity2(ecoreMM, mutatedOriginal, gptMutated));
				} catch (Exception e) {
					System.err.println("An error occurred with file: " + file);
					//e.printStackTrace();
				}
			});
		} catch (IOException e) {
			System.err.println("An error occurred accessing folder: " + folder);
			//e.printStackTrace();
		}
	}

	public static Resource registerMetamodel(String ecoreMetamodel) {
		Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap().put("ecore", new EcoreResourceFactoryImpl());

		ResourceSet rs = new ResourceSetImpl();
		// enable extended metadata
		final ExtendedMetaData extendedMetaData = new BasicExtendedMetaData(rs.getPackageRegistry());
		rs.getLoadOptions().put(XMLResource.OPTION_EXTENDED_META_DATA, extendedMetaData);

		Resource r = rs.getResource(URI.createFileURI(ecoreMetamodel), true);
		for (EObject eObject : r.getContents()) {
			if (eObject instanceof EPackage) {
				EPackage p = (EPackage) eObject;
				registerSubPackage(p);
			}
		}
		return r;
	}

	private static void registerSubPackage(EPackage p) {
		EPackage.Registry.INSTANCE.put(p.getNsURI(), p);
		for (EPackage pack : p.getESubpackages()) {
			registerSubPackage(pack);
		}
	}

	public static double calculateSimilarity2(String metamodel, String art1, String art2) {
		registerMetamodel(metamodel);

		URI uri1 = URI.createFileURI(art1);
		URI uri2 = URI.createFileURI(art2);
		Resource.Factory.Registry.INSTANCE.getExtensionToFactoryMap().put("*", new XMIResourceFactoryImpl());
		ResourceSet resourceSet1 = new ResourceSetImpl();
		ResourceSet resourceSet2 = new ResourceSetImpl();
		resourceSet1.getResource(uri1, true);
		resourceSet2.getResource(uri2, true);

		IComparisonScope scope = new DefaultComparisonScope(resourceSet1, resourceSet2, null);
		int total = 0;
		try {
			Comparison comparisonDef = EMFCompare.builder().build().compare(scope);
			List<Match> matchesDef = comparisonDef.getMatches();
			int counterDef = 0;
			for (Match match : matchesDef) {
				List<Match> lm = new ArrayList<Match>();
				match.getAllSubmatches().forEach(lm::add);
				total += lm.size();
				for (Match match2 : lm) {
					if (match2.getLeft() != null && match2.getRight() != null)
						counterDef++;
				}
				if (match.getLeft() != null && match.getRight() != null)
					counterDef++;
			}
			double value = ((counterDef * 1.0) / total);
			return value;
		} catch (Exception e) {
			return 0;
		}
	}

}
