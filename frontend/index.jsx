import React from 'react';
import ReactDOM from 'react-dom';
import axios from 'axios';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import lightBaseTheme from 'material-ui/styles/baseThemes/lightBaseTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import uuid from 'uuid';


class Application extends React.Component {
  state = {
    room: 'C3PO',
    username: 'calvinfeng',
    message: '',
    payloads: [],
    connected: false
  }

  componentDidMount() {
    this.ws = new WebSocket("ws://" + window.location.host + "/demultiplex/C3PO/?username=" + this.state.username);
    this.eavesdropWS = new WebSocket("ws://" + window.location.host + "/eavesdrop/C3PO/?username=" + this.state.username);
    this.ws.onmessage = this.handleMessage;
    this.eavesdropWS.onmessage = this.handleEavesdropMessage;
    this.ws.onopen = this.handleOpen;
    this.eavesdropWS.onopen = this.handleOpen;
  }

  handleOpen = (e) => {
    this.setState({ connected: true });
  };

  handleEavesdropMessage = (e) => {
    console.log('Eavesdropping shits', e.data);
  };

  handleMessage = (e) => {
    this.setState({ payloads: this.state.payloads.concat([JSON.parse(e.data)]) });
  };

  handleSubmit = (e) => {
    e.preventDefault();
    this.ws.send(JSON.stringify({
      stream: 'message-stream',
      payload: {
        action: 'create',
        data: {
          message: this.state.message,
          username: this.state.username,
          room: this.state.room
        }
      }
    }));
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
      return <p key={uuid()}>Room {payload.room}: {payload.username} said {payload.message}</p>;
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
