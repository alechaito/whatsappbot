<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;

use App\User;
use Auth;
use Hash;

class UserController extends Controller {


    public function insert_agent(Request $request) {
        $user = new User();
        $user->name         = $request->name;
        $user->email        = $request->email;
        $user->password     = Hash::make($request->password);
        $user->leader_id    = Auth::User()->id;
        $user->role         = $request->role;
        $user->save();
        return redirect()->route('home');
    }

    public function insert_admin(Request $request) {
        $user = new User();
        $user->name = $request->name;
        $user->email = $request->email;
        $user->leader_id = $user->id;
        $user->save();
        return redirect()->route('home');
    }


    public function get_all() {
        $user = User::all();
        return User::where('leader_id', Auth::User()->id)->get();
    }

    public function delete($id) {
        $user = User::find($id); 
        if( $user->leader_id == Auth::User()->id ) {
            $user->delete();
        }
        return redirect()->route('home');
    }
}
