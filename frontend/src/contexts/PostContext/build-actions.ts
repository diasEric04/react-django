import { BuildActionsType } from './tsc-types'
import * as actionTypes from './action-type'

export const buildActions: BuildActionsType = ( dispatch ) => {
    return {
        get: () => dispatch({type: actionTypes.GET}),
        post: () => dispatch({type: actionTypes.POST})
    }
}