#pragma once
#include<iostream>
#include <numeric>
#include <algorithm>
#include <omp.h>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
using namespace std;

namespace py = pybind11;
template<typename arr_Type, typename accum_Type>
accum_Type l2norm(const py::array_t<arr_Type>& array){
    py::buffer_info array_info = array.request();
    auto shape = array_info.shape;
    auto size  = std::accumulate(shape.begin(), shape.end(), 1, std::multiplies<int>());
    const arr_Type* array_ptr=static_cast<const arr_Type *>(array_info.ptr);
    return std::accumulate(array_ptr, array_ptr+size, static_cast<accum_Type>(0.0),[](accum_Type a, arr_Type b){return a+b*b;} );
};

template<typename arr_Type, typename accum_Type>
accum_Type l2norm_omp(const py::array_t<arr_Type>& array){
    py::buffer_info array_info = array.request();
    auto shape = array_info.shape;
    auto size  = std::accumulate(shape.begin(), shape.end(), 1, std::multiplies<int>());
    const char* env_threads = std::getenv("OMP_NUM_THREADS");
    int num_threads=1;
    if (env_threads) {
        num_threads= std::stoi(env_threads);
    }
    omp_set_num_threads(num_threads);
    if (size <= num_threads){
        return l2norm<arr_Type, accum_Type>(array);
    }
    auto num_blocks = num_threads + (size % num_threads > 0);
    auto block_size = size/num_threads;
    accum_Type l2sum=0;
    #pragma omp parallel for reduction(+ : l2sum)
      for (int iblock=0; iblock<num_blocks; ++iblock) {
        const arr_Type* first_ptr = static_cast<const arr_Type *>(array_info.ptr)+iblock*block_size;
        const arr_Type* last_ptr = static_cast<const arr_Type *>(array_info.ptr)+(iblock == num_blocks-1? size :(iblock+1)*block_size);
        l2sum+= std::accumulate(first_ptr, last_ptr, static_cast<accum_Type>(0), [](accum_Type a, arr_Type b){return a+b*b;});
      }
    return l2sum;
}

template<typename arr_Type, typename accum_Type>
accum_Type py_functional_norm(const py::array_t<arr_Type>& array, const py::function& function){
    py::buffer_info array_info = array.request();
    auto shape = array_info.shape;
    auto size  = std::accumulate(shape.begin(), shape.end(), 1, std::multiplies<int>());
    const arr_Type* array_ptr=static_cast<const arr_Type *>(array_info.ptr);
    return std::accumulate(array_ptr, array_ptr+size, static_cast<accum_Type>(0.0),
    [function](accum_Type a, arr_Type b){
        py::object py_result = function(a,b);
        return py_result.cast<accum_Type>();} 
    );
};