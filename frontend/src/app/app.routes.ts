import { Routes } from '@angular/router';
import {Test} from './pages/test/test'
import {Home} from './pages/home/home'
export const routes: Routes = [
    {
        path : 'test',
        component : Test,
    },
    {
        path : '',
        component : Home
    },

];
