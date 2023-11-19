import React, { useContext, useState } from 'react';
import { ExperimentTableContext } from '../../context/ExperimentTableContext';

export interface SearchBarProps {
  onSubmit?: (term: string) => void;
}

export const SearchBar = ({ onSubmit }: SearchBarProps) => {
  const { searchFilters, toggleSearchFilter } = useContext(ExperimentTableContext)!;
  const [searchTerm, setSearchTerm] = useState<string>('');

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault(); // Empêche le comportement par défaut
    onSubmit && onSubmit(searchTerm); // Utilise la fonction onSubmit fournie comme prop
  };

  return (
    <div className="searchbar d-flex">
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-auto p-0">
            <div className="dropdown d-flex p-2 w-100 justify-content-center justify-content-lg-start justify-content-xl-start flex-wrap">
              <span className="text-nowrap m-2">Filter By:</span>
              <div className="d-flex">
                {Object.entries(searchFilters).map(([key, filter]) => {
                  return (
                    <div className="dropdown mr-2" key={key} id={key + 'DropdownMenuButton'}>
                      <button
                        className="btn btn-outline-secondary dropdown-toggle p-2 mx-1"
                        type="button"
                        id={key + 'DropdownMenuButton'}
                        data-toggle="dropdown"
                      >
                        {filter.label}
                      </button>
                      <div className="dropdown-menu">
                        {Object.entries(filter.options).map(([name, active]) => (
                          <div className="dropdown-item" key={name} onClick={() => toggleSearchFilter(key, name, !active)}>
                            <div className="form-check">
                              <input
                                checked={active}
                                className="form-check-input"
                                name={key}
                                value={name}
                                type="checkbox"
                                id={key + name + 'checkbox'}
                                onChange={() => toggleSearchFilter(key, name, !active)}
                              />
                              <label className="form-check-label w-100" htmlFor={key}>
                                {name}
                              </label>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
          <div className="col p-0">
            <div className="d-flex flex-fill justify-content-center align-items-center h-100">
              <form className="input-group m-2" method="get" role="form" onSubmit={handleSubmit}>
                <input required name="search_term" type="text" className="form-control" placeholder="Search" value={searchTerm} onChange={handleInputChange}/>
                <div className="input-group-append">
                  <button className="border-0 p-0" type="submit">
                    <i
                      className="fa fa-search input-group-text"
                      style={{ borderTopLeftRadius: 0, borderBottomLeftRadius: 0 }}
                    ></i>
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
