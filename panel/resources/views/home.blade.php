@extends('layouts.app')

@inject('User', 'App\Http\Controllers\UserController')
@php
    $i = 1;
    $agents = $User->get_all();

@endphp
@section('content')
<div class="container">
    <div class="row justify-content-center">
        <div class="col-md-8">
            <div class="card">
                <div class="card-header">Dashboard</div>

                <div class="card-body">
                    @if (session('status'))
                        <div class="alert alert-success" role="alert">
                            {{ session('status') }}
                        </div>
                    @endif

                    <hr>
                    <h2>Representantes</h2>
                    <table class="table">
                        <thead>
                            <tr>
                            <th scope="col">#</th>
                            <th scope="col">Nome</th>
                            <th scope="col">Email</th>
                            <th scope="col">Excluir<th>
                            </tr>
                        </thead>
                        @foreach($agents as $agent)    
                            <tbody>
                                <tr>
                                    <th scope="row"> {{ $i }} </th>
                                    <td> {{ $agent->name }} </td>
                                    <td> {{ $agent->email }} </td>
                                    <td> <a href="{{ route('user.delete', $agent->id) }}"> Excluir </a> </td>
                                </tr>
                            </tbody>
                            @php
                                $i += 1;
                            @endphp
                        @endforeach
                    </table>
                    <hr>
                    <h2>Novo Representante</h2>
                    <form method="POST" action="{{ route('agent.insert') }}">
                        @csrf
                        <div class="form-group">
                            <label for="exampleInputEmail1">Nome</label>
                            <input type="text" class="form-control" name="name" placeholder="Nome Completo">
                        </div>
                        <div class="form-group">
                            <label for="exampleInputEmail1">Email</label>
                            <input type="text" class="form-control" name="email" placeholder="Email">
                        </div>
                        <div class="form-group">
                            <label for="exampleInputEmail1">Senha</label>
                            <input type="password" class="form-control" name="password" placeholder="Senha">
                        </div>
                        <input type="hidden" name="role" value="0"/>
                        <button type="submit" class="btn btn-primary">Adicionar</button>
                    </form>
                </div>
            </div>
        </div>
    </div>
</div>
@endsection
