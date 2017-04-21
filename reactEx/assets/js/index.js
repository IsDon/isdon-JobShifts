import '../css/base.css'
import '../css/lists.css'
//import '../css/bootstrap-datetimepicker.css'
 
var React = require('react')
var ReactDOM = require('react-dom')
//var booties = require("bootstrap-webpack")
var moment = require('moment')

var MAPPING = [ 
		{'uri':'id',
		'header':'Jobs',
		'parentId' : '',
		'fields': ['name']},
		{'uri':'shift',
		'header':'Shifts',
		'parentId' : 'job',
		'fields': ['time_start', 'time_end']},
		{'uri':'role',
		'header':'Positions',
		'parentId' : 'workShift',
		'fields': ['role']}
	];
  
class DjangoCSRFToken extends React.Component {
  render() {
    var csrfToken = Django.csrf_token();
    return React.DOM.input(
      {type:"hidden", name:"csrfmiddlewaretoken", value:csrfToken}
    );
  }
}

class ButtonRemoveItem extends React.Component {
	constructor(props) {
		super(props);
		this.id = this.props.id;
		this.removeFn = this.props.removeFn; //.bind(this,this.id);
	}
	
	render() {
		return (
			<button onClick={this.removeFn}>x</button>
		)
	} 
}

class FormAddItem extends React.Component {
	constructor(props) {
		super(props);
		var top = this.props.top;
		this.addItem = top.addItem.bind(top, this.props.uri['uri']);
		this.fields = this.props.uri['fields'];
	}
	
	render() {			// ref={form => parent.addItemForm = form}	(using e.target)
		var add_str = "add " + this.props.uri['header'];
		var perFieldInputs = this.fields.map(function(item, index){
        	return (
        		<input 
        			name={item} 
        			key={index} 
        			placeholder={item.replace('_', ' ').toLowerCase().replace(/(^| )(\w)/g, s => s.toUpperCase())}>
        		</input>
        	)
        })
        if(this.props.uri['parentId']) {
        	perFieldInputs.push(
        		<input 
	        		type="hidden" 
	        		key={this.fields.length}
	        		name={this.props.uri['parentId']} 
	        		value={this.props.pk}>
	        	</input>
        	)
        }
		return (
			<form onSubmit={this.addItem}>
				<DjangoCSRFToken />
			    <button type="submit">add</button>
			    {perFieldInputs}
			</form>
		)
	}
}

class ItemRow extends React.Component {
	constructor(props) {
		super(props);
		this.fields = this.props.uri[0]['fields'];
	}

	render() {
		let item = this.props.obj;
		let next_list;
		if(item.subList) {
			next_list = <ItemNodes 
				items={item.subList} 
				uri={this.props.uri.slice(1)} 
				top={this.props.top} 
				pk={item.id}
			/>;
		}
		let cur_heading;
		cur_heading = this.fields.map(function(prop, index){
			if(prop.slice(0,5) == 'time_') {
				var options = {
				  year: 'numeric', month: 'numeric', day: 'numeric',
				  hour: 'numeric', minute: 'numeric'
				};
				if(prop == 'time_end') {
					options = {
					  
					  hour: 'numeric', minute: 'numeric',
					  timeZoneName: 'short'
					};
				}
				var datetimestr = new Intl.DateTimeFormat('en-AU', options).format(new Date(item[prop]));
				return (
					<span key={index}>
						{datetimestr}
					</span>
				);
			} else {
				return (
					<span key={index}>
						{item[prop]}
					</span>
				);
			}
		})


		return (
        	<li key={item.id.toString()} >
        		<h3>{cur_heading}</h3>
        		<ButtonRemoveItem id={item.id} removeFn={this.props.removeFn} />
        		{next_list}
        	</li>
		)
	}
}

class ItemNodes extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		var top = this.props.top;
		var pk = this.props.pk;		//id from parent list row
		
		var uri = this.props.uri;
        var perItemNodes =[];
        if(this.props.items) {
        	perItemNodes = this.props.items.map(function(item){
	        	return (
	        		<ItemRow 
		        		key={item.id.toString()} 
		        		obj={item} 
		        		uri={uri} 
		        		top={top} 
		        		removeFn={top.removeItem.bind(top, item.id, uri[0]['uri'])} />
	        	)
	        })
    	}
        return (
            <div className="border">
                <div className="list">
	                <ul>
	                	<li className="header">
			                <h4>{uri[0]["header"]}</h4>
			                <FormAddItem top={top} pk={pk} uri={uri[0]} />
	               		</li>
        				{perItemNodes}
	                </ul>
	            </div>
            </div>
        )
	}
}

class JobsList extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			data:[]
		}
		//bind functions in constructor where required:
		this.loadJobsFromServer = this.loadJobsFromServer.bind(this);
		//this.addItem = this.addItem.bind(this);
	}

    loadJobsFromServer() {
        $.ajax({
            url: this.props.url,
            datatype: 'json',
            cache: false,
            success: function(data) {
                this.setState({data: data});
            }.bind(this)
        })
    }

    addItem(uri, e) {
    	e.preventDefault();
    	var form = e.target;

    	$.ajax({
    		url: this.props.url + uri + '/', // + 'add/',
    		type: 'post',
			data: $(form).serialize(),
    		datatype: 'json',
    		cache: false,
    		success: function(data) {
    			this.loadJobsFromServer();
    		}.bind(this)
    	})
    }

    removeItem(id, uri, e) {
    	console.log('removing item ' + uri + ' @' + id);
    	e.preventDefault();
    	$.ajax({
    		url: this.props.url + uri + '/' + id + '/',
    		type: 'delete',
    		cache: false,
    		success: function(data) {
    			this.loadJobsFromServer();
    		}.bind(this)
    	})
    }

    componentDidMount() {
        this.loadJobsFromServer();
//SETUP: If handling multiple users, enable polling:
        // setInterval(this.loadJobsFromServer, 
        //             this.props.pollInterval)
    }

    componentDidUpdate() {
        $('input[name^=time_]').datetimepicker({
        	sideBySide: true
        });
    }

    render() {
        return (
        	<ItemNodes items={this.state.data} top={this} pk={-1} uri={MAPPING} />
        )
    }
}



ReactDOM.render(<JobsList url='/jobs/api/' pollInterval={20000} />, 
    document.getElementById('JobsAppContainer'))