from neo4jrestclient import GraphDatabase
from models import Flow, Question, Answer

flows = [Flow('morrowind', "Morrowind-style", "A fantasy character creation process like the one at the start of the game Morrowind.")]

def morrowind_flow(start_node):
	q1 = Question(id = 'q1', text = 'What surrounded you when you were young?',
		answers = [Answer(id = 'q1a1', text = 'The sea', reward_type = 'Background', reward_value = 'Coastal'),
			Answer(id = 'q1a2', text = 'Fields', reward_type = 'Background', reward_value = 'Rural'),
			Answer(id = 'q1a3', text = 'Buildings', reward_type = 'Background', reward_value = 'Urban'),
			Answer(id = 'q1a4', text = 'Trees', reward_type = 'Background', reward_value = 'Backwoods'),])
	
	q2 = Question(id = 'q2', text = 'When you were young your family home caught fire. You could hear your mother crying for help inside. How did you save her?',
		answers = [Answer(id = 'q2a1', text = "I seized an axe and cut through the wall of the house, creating an escape route.", reward_type = 'Body', reward_value = '+1'),
			Answer(id = 'q2a2', text ='I gathered up a rope and covered my mouth with a damp cloth. I made my way through the smoke and followed the rope back to safety.', reward_type = 'Mind', reward_value = '+1'),
			Answer(id = 'q2a3', text = 'I charged into the house immediately and found her. We made it out together.', reward_type = 'Spirit', reward_value = '+1')])
	
	q3 = Question(id = 'q3', text = 'You won a prize at your county fair. What was is it that won you this accolade?',
		answers = [Answer(id = 'q3a1', text = 'My skills in archery.', reward_type = 'Skill', reward_value = 'Archery'),
			Answer(id = 'q3a2', text = 'I was a fearless bull leaper.', reward_type = 'Skill', reward_value = 'Acrobatics'),
			Answer(id = 'q3a3', text = 'My horsemanship.', reward_type = 'Skill', reward_value = 'Riding')])
		
	questions = [q1, q2, q3,]
	
	current_questions = start_node.relationships.outgoing(['Question'])
	
	for question in questions:
		if not question.id in [question.end.properties['id'] for question in current_questions]:
			new_question = db.nodes.create(id = question.id, text = question.text)
			start_node.relationships.create('Question', new_question)
			
			for answer in question.answers:
				answer_node = db.nodes.create(id = answer.id, text = answer.text)
				reward_node = db.nodes.create(type = answer.reward_type, value = answer.reward_value)
				answer_node.relationships.create('Reward', reward_node)
				new_question.relationships.create('Answer', answer_node)
		
		
	if len(start_node.relationships.outgoing(['First'])) == 0:
		first_question = [question.end for question in start_node.relationships.outgoing(['Question']) if question.end.properties['id'] == 'q1'][0]
		start_node.relationships.create('First', first_question)
	

db = GraphDatabase("http://localhost:7474/db/data/")

root = db.node[0]

existing_flows =  root.relationships.outgoing(["Flow"])


flow_roots = {}

for flow in flows:
	if not len([link for link in existing_flows if link.properties['title'] == flow.title]) > 0:
		new_flow_node = db.nodes.create(id = flow.id, title = flow.title, description = flow.description)
		root.relationships.create("Flow", new_flow_node)
		
		print "Created new Flow: %s" % flow.title
		
		flow_roots[flow.id] = new_flow_node

morrowind_flow([rel.end for rel in root.relationships.outgoing(["Flow"]) if rel.end.properties['id'] == 'morrowind'][0])
