import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';


class Application extends React.Component {
  state = {
    room: 'C3PO',
    username: 'calvinfeng',
    message: '',
    payloads: [],
    connected: false
  }

  componentDidMount() {
    this.ws = new WebSocket("ws://" + window.location.host + "/C3PO/?username=" + this.state.username);
    this.ws.onmessage = this.handleMessage;
    this.ws.onopen = this.handleOpen;
  }

  handleOpen = (e) => {
    this.setState({ connected: true });
  }

  handleMessage = (e) => {
    this.setState({ payloads: this.state.payloads.concat([JSON.parse(e.data)]) });
  }

  handleSubmit = (e) => {
    e.preventDefault();
    this.ws.send(this.state.message);
  }

  createTextFieldChangeHandler = (fieldName) => {
    return (e, val) => {
      const newState = Object.assign({}, this.state);
      newState[fieldName] = val;
      this.setState(newState);
    };
  };

  get messages() {
    return this.state.payloads.map((payload) => {
      return <p>Room {payload.room}: {payload.username} said {payload.text}</p>;
    });
  }

  render() {
    return (
      <MuiThemeProvider muiTheme={getMuiTheme(lightBaseTheme)}>
        <div>
          {this.messages}
          <form onSubmit={this.handleSubmit}>
            <TextField hintText="message" onChange={this.createTextFieldChangeHandler('message')} /><br />
            <input type="submit" label="Submit" />
          </form>
        </div>
      </MuiThemeProvider>
    )
  }
}

document.addEventListener("DOMContentLoaded", () => {
    ReactDOM.render(<Application />, document.getElementById('react-application'));
});
