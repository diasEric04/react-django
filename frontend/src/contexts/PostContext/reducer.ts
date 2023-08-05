import { ReducerType } from './tsc-types'
import * as types from './action-type'

export const reducer : ReducerType = (state, action) => {
    switch (action.type) {
        case types.START_GET:
            return {...state, loading: true}

        case types.END_GET:
            return {...state, loading: false}

        case types.GET:
            // get dados da api
            return {...state}
        
        case types.POST:
            // post de dados da api
            return {...state}
    }

    return {...state}
}