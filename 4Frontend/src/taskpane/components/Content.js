import * as React from 'react';
import {PrimaryButton, TextField, Spinner} from 'office-ui-fabric-react';

let input_text = "";
export default class Content extends React.Component {
    click = async () => {
        return Word.run(async context => {

            let input = input_text.split("⚫");
            if (input.length < 2) {
                document.getElementById("input").value = "Please enter Words that support your text divided by Tabstopps!"
            }
            else{
                let data = {"text":input};
                //send the data to backend
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
            }
        });
    };

    render() {
        //handle input in textfield, replace tabs
        $('.tdtg-content__input').on('keydown', function(e) {
            if (e.keyCode == 9) {
                e.preventDefault();
                document.getElementById('input').value=document.getElementById('input').value + " ⚫ ";
             }
        });

        return(
            <div class="ms-welcome__main">
                <TextField className='tdtg-content__input' id="input" multiline resizable={false} rows={29} defaultValue={input_text} onChanged={newValue => (input_text=newValue)}/>
                <PrimaryButton className='tdtg-content__button' id='button' iconProps={{ iconName: 'ChevronRight'}} onClick={this.click}>Generate!</PrimaryButton>
                <Spinner className='tdtg-content__spinner' id='spinner' label=" Thinking..." labelPosition="right" />
            </div>
        );
    }
}