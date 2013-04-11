
//INITIALIZE EMBER APP
var App = Ember.Application.create();
//SET UP EMBER ROUTES
App.Router.map(function() {
  this.resource('projects', function() {
    this.resource('project', {
      path: ':project_id'
    });
  });
});

App.IndexRoute = Ember.Route.extend({
  redirect: function(){
    this.transitionTo('projects');
  }
});
App.ApplicationRoute = Ember.Route.extend({
  setupController: function() {
  }
});

App.ProjectsRoute = Ember.Route.extend({
  model: function() {
    return App.Project.find();
  }
});
//MODEL AND ARRAY CONTROLLERS
App.ProjectsController = Ember.ArrayController.extend({
	sortProperties: ['last_name']
});

App.ProjectController = Ember.ObjectController.extend({
	needs:["docs","notes","deposit"],
	addPublicNote: function(project){
  note = this.get('notes');
	note.createRecord({
  author:"Steve Grammer",
	post_date: "03/21/2013",
	body: $('.noteForm').val(),
	internal: false
  });
  $('.noteForm').val("")
	},
	addPrivateNote: function(){
	note = this.get('notes');
	note.createRecord({
  author:"Steve Grammer",
	post_date: "03/21/2013",
	body: $('.noteForm').val(),
	internal: true
  });
  $('.noteForm').val("")
	},
	createDoc: function(doc){
	requested_document = this.get('docs');
	requested_document.createRecord({
	id:1,
	title: doc,
	requested_on: "3/21/2013",
	url: "",
	exists: false
	});
  },
	deleteDoc: function(doc){
    console.log("delete" + doc.get('title'));
    console.log(doc.get('isDeleted'));
  },
  uploadDoc: function(doc){
    window.open( "document-uploader.html" )
  console.log("upload" + doc.get('title'));
  console.log(doc.get('isDeleted'));
}
  });


App.DocsController = Ember.ArrayController.extend({
  needs: ["project"],
  sortProperties: ['title']
});

App.listController = Ember.ArrayProxy.create({
    content: ["Cash","Lines of Credit", "Home Equity", "401K", "Pension", "IRA", "Stocks&Bonds","CD","Life Insurance"]
});

App.NotesController = Ember.ArrayController.extend({
	needs: ["project"]
});
App.DepositController = Ember.ObjectController.extend({

});
//EMBER DATA CONNECTOR
App.Store = DS.Store.extend({
  revision: 11
});

//MODELS
App.Project = DS.Model.extend({
  deposit: DS.belongsTo('App.Deposit'),
  docs: DS.hasMany('App.Doc'),
  notes: DS.hasMany('App.Note'),
  last_name: DS.attr('string'),
  first_name: DS.attr('string'),
  concept: DS.attr('string'),
  store_size: DS.attr('number'),
  sales_rep: DS.attr('string'),
  funding_advisor: DS.attr('string'),
  ad_source: DS.attr('string'),
  social_security_number: DS.attr('string'),
  place_of_employment: DS.attr('string'),
  years_at_job: DS.attr('number'),
  salary: DS.attr('number'),
  app_date: DS.attr('string'),
  app_number: DS.attr('string'),
  email: DS.attr('string'),
  phone_number: DS.attr('string'),
  street_address: DS.attr('string'),
  city: DS.attr('string'),
  state: DS.attr('string'),
  zip_code: DS.attr('string'),
  signature: DS.attr('string'),
  payment_status:  DS.attr('string'),
  required_documents:  DS.attr('string'),
  progress: DS.attr('number'),
  full_name: function() {
    return this.get('first_name') +
           " " + this.get('last_name');
  }.property('first_name', 'last_Name'),
  progressBar: function() {
    return "width:" + this.get('progress') + "%";
  }.property('progress')

});

App.Doc = DS.Model.extend({
	project: DS.belongsTo('App.Project'),
	title: DS.attr('string'),
	requested_on: DS.attr('string'),
	url: DS.attr('string'),
	exists: DS.attr('boolean')
});

App.Note = DS.Model.extend({
	project:DS.belongsTo('App.Project'),
	author: DS.attr('string'),
	post_date: DS.attr('string'),
	body: DS.attr('string'),
	internal: DS.attr('string')
});

App.Deposit = DS.Model.extend({
	project: DS.belongsTo('App.Project'),
	amount: DS.attr('number'),
	status: DS.attr('string'),
	trace_number: DS.attr('string')
});


//TEMPLATE HELPERS

//TEST DATA
App.Note.FIXTURES = [{
	id:1,
	author:"Steve Grammer",
	post_date: "01/26/2011",
	body: "however, in speaking with Neal (Broker) this morning I was told that the 2600 sq. ft. site (end cap) currently has 2 LOIs on it ranging from 38.00 to 42.00 per sq. ft. and landlord is not interested in the Dollar concept due to the Anchor restrictions (Home Goods).",
	internal: false
},{
	id:2,
	author:"Steve Grammer",
	post_date: "01/26/2011",
	body: "however, in speaking with Neal (Broker) this morning I was told that the 2600 sq. ft. site (end cap) currently has 2 LOIs on it ranging from 38.00 to 42.00 per sq. ft. and landlord is not interested in the Dollar concept due to the Anchor restrictions (Home Goods).",
	internal: false
},
{
	id:3,
	author:"Steve Grammer",
	post_date: "01/26/2011",
	body: "however, in speaking with Neal (Broker) this morning I was told that the 2600 sq. ft. site (end cap) currently has 2 LOIs on it ranging from 38.00 to 42.00 per sq. ft. and landlord is not interested in the Dollar concept due to the Anchor restrictions (Home Goods).",
	internal: false
}
];



App.Doc.FIXTURES = [{
	id:1,
	title: "401k",
	requested_on: "01/01/2012",
	url: "/docs/file.pdf",
	exists: true
},
{
	id:2,
	title: "Home Equity",
	requested_on: "01/01/2012",
	url: "/docs/file.pdf",
	exists: true
},
{
	id:3,
	title: "IRA",
	requested_on: "01/01/2012",
	url: "/docs/file.pdf",
	exists: false
},
{
	id:4,
	title: "Stocks/Bonds",
	requested_on: "01/01/2001",
	url: "/docs/file.pdf",
	exists: false
},
{
	id:5,
	title: "CD",
	requested_on: "01/01/2001",
	url: "/docs/file.pdf",
	exists: false
}];

App.Project.FIXTURES = [{
  id: 1,
  last_name: "Rogers",
  first_name: "Buck",
  concept: "Dollar Store Services",
  sales_rep: "Aman Andom",
  app_date: "1/06/2013",
  store_size: 1500,
  app_number: "5734734573",
  email: "castle.63@osu.edu",
  phone_number: "(300)-555-5555",
  street_address:"2292 Adriatic Drive",
  city: "Henderson",
  state: "Nevada",
  zip_code: "89074",
  social_security_number: "555-555-5555",
  place_of_employment: "Timken Company",
  years_at_job: 25,
  salary: 25000,
  signature: "Awaiting Primary",
  payment_status:  "Paid on 02/06/2013",
  required_documents:  "2 of 4 Documents",
  progress: 100,
  docs: [1,2,3,4,5],
  notes:[1,2,3]
},
{
  id: 2,
  last_name: "Smith",
  first_name: "Buck",
  concept: "Dollar Store Services",
  store_size: 1500,
  sales_rep: "Robert Mugabe",
  app_date: "12/06/2012",
  app_number: "5734734573",
  email: "castle.63@osu.edu",
  phone_number: "(300)-555-5555",
  street_address:"2292 Adriatic Drive",
  city: "Henderson",
  state: "Nevada",
  zip_code: "89074",
  social_security_number: "555-555-5555",
  place_of_employment: "Timken Company",
  years_at_job: 25,
  salary: 25000,
  signature: "Awaiting Primary",
  payment_status:  "Paid on 02/06/2013",
  required_documents:  "1 of 4 Documents",
  progress: 40,
  docs: [1,2,3]

},
{
  id: 3,
  last_name: "Buckley",
  first_name: "Maxwell",
  concept: "The Mail Box Stores",
  store_size: 1500,
  sales_rep: "Aman Andom",
  app_date: "12/06/2012",
  app_number: "5734734573",
  signature: "Awaiting Primary",
  email: "castle.63@osu.edu",
  phone_number: "(300)-555-5555",
  social_security_number: "555-555-5555",
  place_of_employment: "Timken Company",
  years_at_job: 25,
  salary: 25000,
  street_address:"2292 Adriatic Drive",
  city: "Henderson",
  state: "Nevada",
  zip_code: "89074",
  payment_status:  "Paid on 02/06/2013",
  required_documents:  "0 of 4 Documents",
  progress: 30
},
{
  id: 4,
  last_name: "Walters",
  first_name: "Mack",
  concept: "Fitness Center Developers",
  sales_rep: "António de Oliveira Salazar",
  funding_advisor: "Funding Advisor",
  app_date: "12/06/2012",
  app_number: "5734734573",
  signature: "Awaiting Primary",
  email: "castle.63@osu.edu",
  phone_number: "(300)-555-5555",
  social_security_number: "555-555-5555",
  place_of_employment: "Timken Company",
  years_at_job: 25,
  salary: 25000,
  street_address:"2292 Adriatic Drive",
  city: "Henderson",
  state: "Nevada",
  zip_code: "89074",
  payment_status:  "Paid on 02/06/2013",
  required_documents:  "1 of 4 Documents",
  progress: 50
},
{
  id: 5,
  last_name: "Johnson",
  first_name: "Smiles",
  concept: "Dollar Store Services",
  sales_rep: "Eduardo Lonardi",
  app_date: "12/06/2012",
  app_number: "5734734573",
  email: "castle.63@osu.edu",
  phone_number: "(300-555-5555)",
  social_security_number: "555-555-5555",
  place_of_employment: "Timken Company",
  years_at_job: 25,
  salary: 25000,
  street_address:"2292 Adriatic Drive",
  city: "Henderson",
  state: "Nevada",
  zip_code: "89074",
  signature: "Awaiting Primary",
  payment_status:  "Paid on 02/06/2013",
  required_documents:  "3 of 4 Documents",
  progress: 20
}
];

//Animations and PopOvers
