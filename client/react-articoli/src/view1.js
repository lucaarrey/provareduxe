import React, { Component } from 'react';

class View1 extends React.Component {
    constructor(props){
        super(props);
    }


}



export default View1;



function getArticles() {
     fetch('http://127.0.0.1:5000/articles/')
        .then(function (response) {
            if (response.ok) {
                return response.json();
            }
            throw new Error('Network response was not ok.');
        })
        .then(function(jsonData){
            console.log(jsonData);
        })
}