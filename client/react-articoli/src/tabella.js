import React, { Component } from 'react';

var ARTICOLI = [
    {title: 'titolo',
    content: 'Contenuto'},
    {title: 'titolo2',
    content: 'Contenuto2'},
    {title: 'titolo3',
    content: 'Contenuto3'}
    ]

var LISTAVUOTA = []

class Articles extends React {
    constructor(props) {
        super(props);
        //articles =
        this.state = {};
}
    componentDidMount() {
       return fetch('http://127.0.0.1:5000/articles/')
       .then(function (response) {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(function(jsonData){
            console.log(jsonData);
            let title = <th>{jsonData.title}</th>
            let content =<th>{jsonData.content}</th>
        })
    }

    render() {

        return (
            <tr>
                <th>this.state..</th>
                <th>this.state..</th>
            </tr>

            )
    }
}

class Tabella extends Component {
    render() {
    var rows = ARTICOLI.map(
        el => {
            return (
                <tr>
                    <td>{el.title}</td>
                    <td>{el.content}</td>
                </tr>
            );
        }
    );

    return (
      <table>
        <thead>
          <tr>
            <th>Title</th>
            <th>Contenuto</th>
            <th>______</th>
          </tr>
        </thead>
        <tbody>{rows}</tbody>
      </table>
    );
  }
}

export default Tabella, Articles;