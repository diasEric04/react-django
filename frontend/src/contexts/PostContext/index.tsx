import { createContext, useReducer, useContext, useRef } from 'react';
import { StateType, ContextType, ContextProviderType } from './tsc-types';
import { reducer } from './reducer';
import { buildActions } from './build-actions';

export const initialState : StateType = {
    posts: [],
    loading: false   
}

const Context = createContext<ContextType>({} as ContextType)


export const PostContextProvider : ContextProviderType = ({ children }) => {
    const [postState, postDispatch] = useReducer(reducer, initialState)
    const actions = useRef(buildActions(postDispatch))
    return (
        <Context.Provider value={{postState, actions: actions.current}}>
            {children}
        </Context.Provider>
    )
}

export const usePostContext = () => {
    const context = useContext(Context)

    if (JSON.stringify(context) === "{}") {
        throw new Error('you have to use useCounterContext inside <CounterContextProvier/>')
    }

    return {...context}
}