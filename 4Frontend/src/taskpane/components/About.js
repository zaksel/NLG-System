import * as React from 'react';
import {Label} from 'office-ui-fabric-react';

export default class About extends React.Component {
    render() {
        const {
            title,
            logo,
            message
        } = this.props;

        return (
            <section className='ms-welcome__header ms-u-fadeIn500'>
                <img width='90' height='90' src={logo} alt={title} title={title} />
                <Label className='ms-fontSize-su ms-fontWeight-light ms-fontColor-neutralPrimary'>{title}</Label>
                <Label className='ms-about__text'>{message}</Label>
            </section>
        );
    }
}