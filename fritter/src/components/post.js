import React from 'react'
import styled, { css } from 'styled-components'

function post(props) {

  console.log("IN POST")

  return (
    <div>
      <div>
        <div>
          <strong>@</strong>{props.author}
        </div>
        <div>
          {props.created}
        </div>
      </div>
      {props.body}
    </div>
  )

}

export default post;
