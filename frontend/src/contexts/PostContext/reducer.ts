import { ReducerType } from './tsc-types'
import * as types from './action-type'

export const reducer : ReducerType = (state, action) => {
    switch (action.type) {
        case types.START_GET:
            return {...state, loading: true}

        case types.END_GET:
            return {...state, loading: false}

        case types.SET_POSTS:
            return {...state, posts: action.payload ?? []}
    }

    return {...state}
}