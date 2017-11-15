package services.similarity.similarity;

import services.similarity.ontologyManagement.MyOWLLogicalEntity;
import services.similarity.ontologyManagement.OWLConcept;

public interface ComparableElement {
	double similarity(ComparableElement a, MyOWLLogicalEntity org, MyOWLLogicalEntity des) throws Exception;
	//String getId();
}
