import * as React from 'react';
import {Button, ButtonType, Label, TextField, Spinner} from 'office-ui-fabric-react';

export default class Content extends React.Component {
    click = async () => {
        return Word.run(async context => {

            let input = document.getElementById("input").value;
            //process the inputs
            let lines = input.split("\n");
            let words =[];
            lines.forEach(function (line, index) {
                words.push(line)
            });
            let data = {"words":words};

            //send the inputs to backend
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/input",
                data : JSON.stringify(data),
                dataType: 'json',
                beforeSend: function() {
                    document.getElementById('button').style.visibility="collapse";
                    document.getElementById('spinner').style.visibility="visible"
                },
                complete: function() {
                    document.getElementById('button').style.visibility="visible";
                    document.getElementById('spinner').style.visibility="collapse"
                },
                success : async function(res) {
                    let text = res.text;
                    let paras = text.split("\n");
                    paras.forEach(function(paragraph) {
                        const written = context.document.body.insertText(paragraph, Word.InsertLocation.end);
                        written.font.color = "blue";
                        const test = context.document.body.insertBreak("Line","End");
                    });
                    await context.sync();
                }
            });
        });
    };


    render() {
        return(
            <div class="ms-welcome__main">
                <TextField className='tdtg-content__input' id="input" multiline resizable={false} rows={29}/>
                <Button className='tdtg-content__button' id='button' iconProps={{ iconName: 'ChevronRight'}} onClick={this.click}>Generate!</Button>
                <Spinner className='tdtg-content__spinner' id='spinner' label=" Thinking..." ariaLive="assertive" labelPosition="right" />
            </div>
        );
    }
}