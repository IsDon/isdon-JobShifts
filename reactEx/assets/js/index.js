import '../css/base.css'
import '../css/lists.css'
 
var React = require('react')
var ReactDOM = require('react-dom')
//var booties = require("bootstrap-webpack")
var moment = require('moment')

function Action(uri, type='normal', action='get', tooltip='') {
    this.uri=uri;
    this.type=type;
    this.action=action;
    this.tooltip=tooltip;
}
var MAPPING_Admin = [
        {
            'uri':'id',
            'header':'Jobs',
            'remove':new Action('job'),
            'add':new Action('job'),
            'click':false,
            'parentId' : '',
            'fields': ['name'],
            'fields_input': ['name']
        },
        {
            'uri':'shift',
            'header':'Shifts',
            'remove':new Action('shift'),
            'add':new Action('shift'),
            'click':false,
            'parentId' : 'job',
            'fields': ['time_start', 'time_end'],
            'fields_input': ['time_start', 'time_end']
        },
        {
            'uri':'role',
            'header':'Positions Required',
            'remove':new Action('role'),
            'add':new Action('role'),
            'click':new Action('jobs/api/role/open','modal','patch', 'Open for Filling'),
            'parentId' : 'workShift',
            'fields': ['role', 'get_status_display'],
            'fields_input': ['role']
        },
        {
            'uri':'',
            'header':'Staff Responses',
            'remove':false,
            'add':false,
            'click':false,
            'parentId' : 'role',
            'fields': ['staff_name', 'get_status_display'],
            'fields_input': []
        }
    ];

var MAPPING_ShiftWorker = [ 
        {
            'uri':'id',
            'header':'Jobs',
            'remove':false,
            'add':false,
            'click':false,
            'parentId' : '',
            'fields': ['name'],
            'fields_input': ['name']
        },
        {
            'uri':'shift',
            'header':'Shifts',
            'remove':false,
            'add':false,
            'click':false,
            'parentId' : 'job',
            'fields': ['time_start', 'time_end'],
            'fields_input': ['time_start', 'time_end']
        },
        {
            'uri':'role',
            'header':'Positions Required',
            'remove':false,
            'add':false,
            'click':new Action('responses/api/accept','modal','patch', 'Mark as Available'),
            'parentId' : 'workShift',
            'fields': ['role', 'get_status_display'],
            'fields_input': ['role']
        },
        {
            'uri':'',
            'header':'Responses',
            'remove':false,
            'add':false,
            'click':new Action('responses/api/revoke','modal','patch', 'Remove Availability'),
            'parentId' : 'role',
            'fields': ['staff_name', 'get_status_display'],
            'fields_input': []
        }
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
        this.addItem = top.addItem.bind(top, this.props.uri['add']['uri']);
        this.fields = this.props.uri['fields_input'];
    }
    
    render() {          // ref={form => parent.addItemForm = form}  (using e.target)
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
        if((item.subList && item.subList.length) || (this.props.uri.length>1 && this.props.uri[1]['add'])) {
            next_list = <ItemNodes 
                items={item.subList} 
                uri={this.props.uri.slice(1)} 
                top={this.props.top} 
                pk={item.id}
            />;
        }
        let cur_heading;    //full row of descriptive text spans
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
        let formRemoveButton;
        if(this.props.uri[0]['remove']) formRemoveButton = <ButtonRemoveItem id={item.id} removeFn={this.props.removeFn} />;
        
        if(this.props.uri[0]['click']) {  //add onClick binding:
            var clickFn = this.props.top.handleClick.bind(
                this.props.top, 
                item.id, 
                this.props.uri[0]['click']
            );
            var clickTooltip = this.props.uri[0]['click']['tooltip'];
            return (
                <li key={item.id.toString()}>
                    <h3 onClick={clickFn} className="pointer" title={clickTooltip}>
                        {cur_heading}
                    </h3>
                    {formRemoveButton}
                    {next_list}
                </li>
            )
        } else {
            return (
                <li key={item.id.toString()} >
                    <h3>{cur_heading}</h3>
                    {formRemoveButton}
                    {next_list}
                </li>
            )
        }
    }
}

class ItemNodes extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        var top = this.props.top;
        var pk = this.props.pk;     //id from parent list row
        
        var uri = this.props.uri;
        let perItemNodes;
        if(this.props.items) {
            perItemNodes = this.props.items.map(function(item){
                return (
                    <ItemRow 
                        key={item.id.toString()} 
                        obj={item} 
                        uri={uri} 
                        top={top} 
                        removeFn={top.removeItem.bind(top, item.id, uri[0]['remove']['uri'])} />
                )
            })
        }
        let formAddItem;
        if(uri[0]['add']) formAddItem = <FormAddItem top={top} pk={pk} uri={uri[0]} />;
        var listclasses = `${uri[0]["header"].split(" ")[0].toLowerCase()}`;
        return (
            <div className="border">
                <div className={"list " + listclasses}>
                    <ul>
                        <li className="header">
                            <h4>{uri[0]["header"]}</h4>
                            {formAddItem}
                        </li>
                        {perItemNodes}
                    </ul>
                </div>
            </div>
        )
    }
}

class ItemList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            data:[]
        }
        //bind functions in constructor where required:
        this.loadDataFromServer = this.loadDataFromServer.bind(this);
        //this.addItem = this.addItem.bind(this);
    }

    loadDataFromServer() {
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
                this.loadDataFromServer();
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
                this.loadDataFromServer();
            }.bind(this)
        })
    }

    handleClick(id, action, e) {
        console.log('click action');
        e.preventDefault();
        var csrfToken = Django.csrf_token();
        var data_csrf = {};
        data_csrf["csrfmiddlewaretoken"]=csrfToken;
        $.ajax({
            url: action.uri + '/' + id + '/',
            type: 'get', // action.action,
            contentType:"application/json",
            //data: JSON.stringify(data_csrf),
            cache: false,
            success: function(data) {
                this.loadDataFromServer();
            }.bind(this)
        })
    }

    componentDidMount() {
        this.loadDataFromServer();
//SETUP: If handling multiple users, enable polling:
        // setInterval(this.loadDataFromServer, 
        //             this.props.pollInterval)
    }

    componentDidUpdate() {
        $('input[name^=time_]').datetimepicker({
            sideBySide: true
        });
    }

    render() {
        return (
            <ItemNodes items={this.state.data} top={this} pk={-1} uri={this.props.map} />
        )
    }
}

var app_root = document.getElementById('JobsAppContainer');
if($(app_root).hasClass('admin')) {
    ReactDOM.render(<ItemList url='/jobs/api/' pollInterval={10000} map={MAPPING_Admin} />, 
        document.getElementById('JobsAppContainer'))
} else {
    ReactDOM.render(<ItemList url='/responses/api/' pollInterval={30000} map={MAPPING_ShiftWorker} />, 
        document.getElementById('JobsAppContainer'))
}