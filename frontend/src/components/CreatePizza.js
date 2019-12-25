import React, { Component } from 'react';

class CreatePizza extends Component{
    render(){

        const pizza_type =
            <label>Pizza Type<input type="text" name="type"/> </label>;

        const pizza_size=
            <label >Size
            <select id="pizza-size" name="pizza-type">
                <option value="S">S</option>
                <option value="M">M</option>
                <option value="L">L</option>
            </select></label>;

        const pizza_amount = 
            <label>Pizza Amount<input type="number" name="amount"/></label>;
            return (
                <div>
                     {pizza_type}<br/>
                     {pizza_amount}<br/>
                     {pizza_size}
                </div>
            );
    }
}

export default CreatePizza;
