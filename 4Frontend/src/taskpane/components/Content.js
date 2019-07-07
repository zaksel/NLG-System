import * as React from 'react';
import {Button, ButtonType, Label, TextField} from 'office-ui-fabric-react';

export default class Content extends React.Component {
    click = async () => {
        return Word.run(async context => {

            let input = document.getElementById("input").value;
            //process the inputs
            //let lines = input.split("\n");
            input = {
                "word":input,
                "length": 23
            };

            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:5000/input",
                data : JSON.stringify(input),
                dataType: 'json',
                success : async function(res) {
                    let text = res.text;
                    const paragraph = context.document.body.insertParagraph(text, Word.InsertLocation.end);
                    paragraph.font.color = "blue";
                    await context.sync();
                }
            });
        });
    };


    render() {
        return(
            <div class="ms-welcome__main">
                <TextField className='tdtg-content_input' id="input" multiline resizable={false} rows={29}/>
                <Button className='ms-welcome__action' iconProps={{ iconName: 'ChevronRight' }} onClick={this.click}>Generate!</Button>
            </div>
        );
    }
}