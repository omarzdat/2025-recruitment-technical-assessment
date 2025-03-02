import React from 'react';
import { Search, LayoutGrid, Map, Moon, Filter, SlidersHorizontal } from 'lucide-react';

const FreeroomsApp = () => {
  
  // a lil bit of mock data, added total to express color as a percentage of rooms available
  const buildings = [
    { id: 1, name: 'AGSM', available: 9, total: 9, image: 'src/assets/agsm.webp' },
    { id: 2, name: 'Ainsworth Building', available: 0, total: 16, image: 'src/assets/ainsworth.webp' },
    { id: 3, name: 'Anita B Lawrence Centre', available: 35, total: 44, image: 'src/assets/anitab.webp' },
    { id: 4, name: 'Biological Sciences', available: 2, total: 6, image: 'src/assets/biologicalScience.webp' },
    { id: 5, name: 'Biological Sciences (West)', available: 7, total: 8, image: 'src/assets/biologicalScienceWest.webp' },
    { id: 6, name: 'Blockhouse', available: 3, total: 42, image: 'src/assets/blockhouse.webp' },
    { id: 7, name: 'Business School', available: 1, total: 18, image: 'src/assets/businessSchool.webp' },
    { id: 8, name: 'Civil Engineering Building', available: 6, total: 8, image: 'src/assets/civilBuilding.webp' },
    { id: 9, name: 'Colombo Building', available: 5, total: 5, image: 'src/assets/colombo.webp' },
    { id: 10, name: 'Computer Science & Eng (K17)', available: 3, total: 7, image: 'src/assets/cseBuilding.webp' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header/Navbar */}
      <header className="border-b border-gray-200 bg-white">
        <div className="w-full px-4 py-2 flex justify-between items-center">
          {/* Logo */}
          <div className="text-orange-500 font-bold text-2xl flex items-center">
            <img 
              src="/src/assets/freeRoomsLogo.png" 
              alt="Freerooms Logo" 
              className="w-8 h-8 mr-2" 
            />
            Freerooms
          </div>
          
          {/* Navigation Icons */}
          <div className="flex space-x-2">
            <button className="p-2 border border-orange-200 rounded-md text-orange-500">
              <Search size={24} />
            </button>
            <button className="p-2 border border-orange-200 rounded-md bg-orange-500 text-white">
              <LayoutGrid size={24} />
            </button>
            <button className="p-2 border border-orange-200 rounded-md text-orange-500">
              <Map size={24} />
            </button>
            <button className="p-2 border border-orange-200 rounded-md text-orange-500">
              <Moon size={24} />
            </button>
          </div>
        </div>
      </header>

      {/* Search and Filters */}
      <div className="w-full p-4">
        <div className="flex justify-between items-center mb-6">
          {/* Filters Button */}
          <button className="flex items-center space-x-2 px-4 py-2 border border-orange-500 text-orange-500 rounded-md">
            <Filter size={20} />
            <span>Filters</span>
          </button>
          
          {/* Search Bar */}
          <div className="flex-1 mx-4">
            <div className="relative">
              <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                <Search size={20} className="text-gray-400" />
              </div>
              <input
                type="text"
                placeholder="Search for a building..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:border-orange-500 focus:ring-1 focus:ring-orange-500"
              />
            </div>
          </div>
          
          {/* Sort Button */}
          <button className="flex items-center space-x-2 px-4 py-2 border border-orange-500 text-orange-500 rounded-md">
            <SlidersHorizontal size={20} />
            <span>Sort</span>
          </button>
        </div>

        {/* Building Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          {buildings.map((building) => (
            <div key={building.id} className="bg-white rounded-lg overflow-hidden shadow-md">
              {/* Building Image */}
              <div className="relative h-85 bg-gray-200">
                <img
                  src={building.image}
                  alt={building.name}
                  className="w-full h-full object-cover"
                />
                
                {/* Availability Badge */}
                <div className="absolute top-3 right-3 bg-white rounded-full py-1 px-3 flex items-center shadow-md">
                  {/* cant say this was all me but looking at other sites to learn about it was so fun */}
                  <div className={`w-2 h-2 rounded-full mr-2 ${
                    building.available / building.total === 0 
                      ? 'bg-red-500'
                      : building.available / building.total <= 0.5 
                        ? 'bg-yellow-500' 
                        : 'bg-green-500'
                  }`}></div>
                  <span className="text-sm">
                    {building.available === 1 ? `1 room available` : `${building.available} rooms available`}
                  </span>
                </div>

                {/* Building Name */}
                <div className="absolute m-auto bottom-3 left-3 right-3 rounded-md bg-orange-500 text-white p-3 text-lg">
                  {building.name}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default FreeroomsApp;