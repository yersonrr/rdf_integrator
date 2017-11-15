package services.similarity.ontologyManagement;

import org.semanticweb.owlapi.model.OWLDataProperty;
import org.semanticweb.owlapi.model.OWLObjectProperty;
import org.semanticweb.owlapi.model.OWLProperty;

public class OWLRelation {
	private OWLProperty p;
	private String uri;
	private MyOWLOntology o;
	
	public OWLRelation(OWLProperty property, MyOWLOntology ont)
	{
		o = ont;
		p = property;
		uri = property.toStringID();
	}
	
	public OWLProperty getOWLProperty()
	{
		return p;
	}
	
	public OWLObjectProperty getOWLObjectProperty()
	{
		return p.asOWLObjectProperty();//o.getOWLObjectProperty(uri);
	}
	
	public int hashCode()
	{
		return uri.hashCode();
	}
	
	public boolean equals(Object o)
	{
		if (o instanceof OWLRelation)
			return equals((OWLRelation) o);
		return false;
	}
	
	public boolean equals(OWLRelation r)
	{
		return uri.equals(r.uri);
	}
	
	public OWLDataProperty getOWLDataProperty()
	{
		return p.asOWLDataProperty();
	}
	
	public String toString()
	{
		return uri;
	}
	
	public double similarity(OWLRelation r)
	{
		return o.taxonomicPropertySimilarity(getOWLProperty(), r.getOWLProperty());
	}
}
