package services.similarity.ontologyManagement;

import java.util.Set;

import org.semanticweb.owlapi.model.OWLLiteral;

import info.debatty.java.stringsimilarity.JaroWinkler;
import services.similarity.similarity.ComparableElement;
import services.similarity.similarity.matching.BipartiteGraphMatching;
import services.similarity.test.ComparisonResult;





public class OWLLink implements ComparableElement {
	private OWLRelation relation;
	private MyOWLLogicalEntity destiny;
	private OWLLiteral desLiteral;
	private Set<OWLExplanation> explanations;
	

	public OWLLink( OWLRelation r, MyOWLLogicalEntity b, Set<OWLExplanation> exp) {
		relation = r;
		destiny = b;
		explanations = exp;
		desLiteral = null;
	}
	
	public OWLLink(OWLRelation r, MyOWLLogicalEntity b) {
		relation = r;
		destiny = b;
		explanations = null;
		desLiteral = null;
	}
	
	public OWLLink(OWLRelation r, OWLLiteral b) {
		relation = r;
		desLiteral = b;
		destiny = null;
		explanations = null;
	}

	public Set<OWLExplanation> getExplanations() {
		return explanations;
	}

	public void setExplanations(Set<OWLExplanation> explanations) {
		this.explanations = explanations;
	}
	
	public String toString()
	{
		if (destiny != null)
			return relation.toString() + " " + destiny.toString();
		else
			return relation.toString() + " " + desLiteral.toString();
	}
	
	public OWLRelation getRelation()
	{
		return relation;
	}
	
	public MyOWLLogicalEntity getDestiny()
	{
		return destiny;
	}
	
	
	public double similarity(OWLLink a, MyOWLLogicalEntity conceptA, MyOWLLogicalEntity conceptB)
	{
		BipartiteGraphMatching bpm = new BipartiteGraphMatching();
		
		try {
			double sim = 0;
			/*double simTaxRel = relation.similarity(a.relation);
			if (simTaxRel == 0)
				sim = 0;
			else
			{
				double simTaxDes = destiny.taxonomicSimilarity(a.destiny);
				double simExp = bpm.matching(explanations, a.explanations, conceptA, conceptB);
				sim = 0.1*simTaxRel + 0.5*simTaxDes + 0.4*simExp;
			}*/
			double simTaxRel = relation.similarity(a.relation);
			double simTaxDes = 0;
			if (destiny != null && a.destiny != null)
				simTaxDes = destiny.taxonomicSimilarity(a.destiny);
			if (desLiteral != null && a.desLiteral != null)
			{
				if (desLiteral.isRDFPlainLiteral() && a.desLiteral.isRDFPlainLiteral())
				{
					JaroWinkler jw = new JaroWinkler();
					simTaxDes = jw.similarity(desLiteral.getLiteral(), a.desLiteral.getLiteral());

				}
				else
					simTaxDes = (desLiteral.equals(a.desLiteral)) ? 1: 0;
			}
			double simExp = 1;//0;
			//if (simTaxRel != 0 && simTaxDes != 0)
			//	simExp = bpm.matching(explanations, a.explanations, conceptA, conceptB);
			sim = (simTaxRel + simTaxDes) / 2;//;*simExp;
			return sim;
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return 0.0;
	}

	public double similarity(ComparableElement a, MyOWLLogicalEntity org, MyOWLLogicalEntity des) throws Exception {
		if (!(a instanceof OWLLink))
			throw new Exception("Invalid comparison");
		return similarity((OWLLink)a, org, des);
	}
	
	public boolean equals(Object o)
	{
		if (o instanceof OWLLink)
			return equals((OWLLink) o);
		return false;
	}
	
	public boolean equals(OWLLink b)
	{
		if (destiny != null)
			return relation.equals(b.relation) && destiny.getName().matches(b.destiny.getName());
		else
		{
			boolean res = relation.equals(b.relation);
			res = res && desLiteral.getLiteral().matches(b.desLiteral.getLiteral()); 
			return res;
		}
	}
	
	public int hashCode(){
		if (destiny != null)
			return relation.hashCode() ^ destiny.hashCode();
		else
			return relation.hashCode() ^ desLiteral.getLiteral().hashCode();
	}

}
