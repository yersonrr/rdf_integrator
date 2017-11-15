package services.similarity.ontologyManagement;

import java.util.HashSet;
import java.util.Set;

import org.semanticweb.owlapi.model.OWLClass;

import org.semanticweb.owlapi.model.OWLLogicalEntity;
import org.semanticweb.owlapi.model.OWLNamedIndividual;

import services.similarity.similarity.matching.BipartiteGraphMatching;
import services.similarity.similarity.matching.OneToManyMatching;


public class MyOWLIndividual extends MyOWLLogicalEntity{
	private OWLNamedIndividual ind;

	
	public MyOWLIndividual(OWLNamedIndividual a, MyOWLOntology onto)
	{
		o = onto;
		uri = a.getIRI().toString();//.toURI().toString();
		neighbors = null;
		ind = a;
	}
	
	public OWLNamedIndividual getOWLNamedIndividual()
	{
		if (ind == null)
			ind = o.getOWLIndividual(uri).asOWLNamedIndividual();
		return ind;
	}
	
	public Set<OWLLink> getNeighbors()
	{
		if (neighbors == null)
			neighbors = o.getIndividualOWLLink(this);
		return neighbors;
	}
	
	
	private double similarityNeighbors(MyOWLIndividual c)
	{
		//BipartiteGraphMatching bpm = new BipartiteGraphMatching();
		OneToManyMatching bpm = new OneToManyMatching();
		if (neighbors == null) {
			neighbors = o.getIndividualOWLLink(this);
			//System.out.println("Nei: "+neighbors);
		}
		if (c.neighbors == null)
			c.neighbors = o.getIndividualOWLLink(c);
		try {
			double sim = bpm.matching(neighbors, c.neighbors, this, c);
			return sim;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return 0.0;
	}
	
	private double similarityNeighbors(OWLConcept c)
	{
		return c.similarityNeighbors(this);
	}
	

	public double similarityNeighbors(MyOWLLogicalEntity c) throws Exception{
		if (c instanceof MyOWLIndividual)
		{
			MyOWLIndividual ind = (MyOWLIndividual) c;
			return this.similarityNeighbors(ind);
		}
		if (c instanceof OWLConcept)
		{
			OWLConcept con = (OWLConcept) c;
			return this.similarityNeighbors(con);
		}
		return 0;
	}
	
	public double taxonomicSimilarity(MyOWLIndividual c)
	{
		return o.taxonomicIndividualSimilarity(getOWLNamedIndividual(), c.getOWLNamedIndividual());
	}
	
	public Set<OWLConcept> getTypes()
	{
		Set<OWLConcept> concepts = new HashSet<OWLConcept>();
		Set<OWLClass> cls = o.getTypes(ind, true);//ind.getTypes(o.getOWLOntology());
		for (OWLClass cl: cls)
		{
			OWLClass namedCl = cl.asOWLClass();
			OWLConcept con = o.getOWLConcept(namedCl.toStringID());
			concepts.add(con);
		}
		return concepts;
		
	}
	
	public double taxonomicSimilarity(OWLConcept c)
	{
		Set<OWLConcept> cls = this.getTypes();
		double sim = 0, max = 0;
		for (OWLConcept con: cls)
		{
			sim = c.taxonomicSimilarity(con);
			if (sim > max)
				max = sim;
		}
		return max;
	}
	
	public double taxonomicSimilarity(MyOWLLogicalEntity c) throws Exception
	{
		if (c instanceof MyOWLIndividual)
				return taxonomicSimilarity((MyOWLIndividual)c);
		if (c instanceof OWLConcept)
			return taxonomicSimilarity((OWLConcept)c);
		else
			throw new Exception("Invalid comparison between " + this + " and " + c);
	}
	
	public boolean isOfType(OWLConcept c)
	{
		return o.isOfType(getOWLNamedIndividual(), c.getOWLClass());
	}
	
	public double getIC()
	{
		return 1;
	}
	
	public double getDepth()
	{
		return o.prof(this.ind);
	}
	
	public double similarity(MyOWLIndividual c, String method) throws Exception
	{
		if (this == c)
			return 1.0;
		
		double sim = 0.0;

        if (method.equals("jaccard"))
		    sim = Jaccard(c);//
        if (method.equals("gades"))
            sim = OnSim(c);//

		return sim;
	}
	
	public OWLConcept getLCA(MyOWLIndividual b)
	{
		return o.getLCS(this, b);
	}

	@Override
	public double similarity(MyOWLLogicalEntity a) throws Exception {
		if (a instanceof MyOWLIndividual)
			return similarity((MyOWLIndividual)a);
		if (a instanceof OWLConcept)
			return similarity((OWLConcept) a);
		throw new Exception("Invalid comparison between " + this + " and " + a);
		
	}
	
	public double similarity(OWLConcept c) throws Exception {
		double taxSim = taxonomicSimilarity(c);
		double neighSim = 1;
		if (taxSim > 0)
			neighSim = similarityNeighbors(c);
		double sim = taxSim*neighSim;
		return sim;
	}

	@Override
	public OWLLogicalEntity getOWLLogicalEntity() {
		return ind;
	}
}
