import React, { Component } from 'react';

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

export default Articles;
