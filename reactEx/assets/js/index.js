import '../css/base.css'
import '../css/lists.css'


var React = require('react')
var ReactDOM = require('react-dom')
  
class DjangoCSRFToken extends React.Component {
  
  render() {

    var csrfToken = Django.csrf_token();

    return React.DOM.input(
      {type:"hidden", name:"csrfmiddlewaretoken", value:csrfToken}
      );
  }
};

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

class FormAddJob extends React.Component {
	constructor(props) {
		super(props);
		this.addJob = this.props.parent.addJob;
	}
	
	render() {
		return (
			<form onSubmit={this.addJob} ref={form => this.props.parent.addJobForm = form}>
				<DjangoCSRFToken />
			    <input name="name" placeholder="add job"></input>
			    <input name="location" type="hidden" placeholder="location" value=""></input>
			    <button type="submit">add</button>
			</form>
		)
	}
}

class JobRow extends React.Component {
	constructor(props) {
		super(props);
	}

	render() {
		let next_list = null;
		let job = this.props.jobObj;
    	if (job.shifts.length) {
    		next_list = <ul>
    			<li>Hello sub-list</li>
    		</ul>;
    	}
		return (
        	<li key={job.id.toString()} >
        		{job.name} 
        		<ButtonRemoveItem id={job.id} removeFn={this.props.removeFn} />
        		{next_list}
        	</li>
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
		this.addJob = this.addJob.bind(this);
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

    addJob(e) {
    	e.preventDefault();
    	$.ajax({
    		url: this.props.url, // + 'add/',
    		type: 'post',
			data: $(this.addJobForm).serialize(),
    		datatype: 'json',
    		cache: false,
    		success: function(data) {
    			this.loadJobsFromServer();
    		}.bind(this)
    	})
    }

    removeJob(id, e) {
    	console.log('removing job ' + id);
    	e.preventDefault();
    	$.ajax({
    		url: this.props.url + 'id/' + id,
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

    render() {
        if (this.state.data) {
        	var self = this;
            var jobNodes = this.state.data.map(function(job){
            	return (
            		<JobRow key={job.id.toString()} jobObj={job} removeFn={self.removeJob.bind(self, job.id)} />
            	)
            })
        }

        return (
            <div>
                <div className="header">
	                <h1>Jobs</h1>
	                <FormAddJob parent={this} />
		        </div>
                <div className="list">
	                <ul>
	                    {jobNodes}
	                </ul>
	            </div>
            </div>
        )
    }
}



ReactDOM.render(<JobsList url='/jobs/api/' pollInterval={20000} />, 
    document.getElementById('container'))