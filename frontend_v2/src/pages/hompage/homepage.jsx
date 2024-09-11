import React from 'react';
import Header from '../../components/header/header.component';
import Body from '../../components/header/body/body.component';
import Footer from '../../components/footer/footer.component';

class Homepage extends React.Component {
    constructor() {
        super();

        this.state = [

        ]
    }

    render () {
        return (
            <div>
                <Header />
                <Body />
                <Footer />
            </div>
        )
    }
}

export default Homepage;