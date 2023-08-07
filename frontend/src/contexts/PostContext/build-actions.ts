import { BuildActionsType } from './tsc-types'
import * as actionTypes from './action-type'

export const buildActions: BuildActionsType = ( dispatch ) => {
    return {
        setPosts: (posts) => dispatch({type: actionTypes.SET_POSTS, payload: posts}),
        startGet: () => dispatch({type: actionTypes.START_GET}),
        endGet: () => dispatch({type: actionTypes.END_GET}),
    }
}