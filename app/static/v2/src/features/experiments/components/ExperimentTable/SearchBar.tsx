import React, { useState } from 'react';

export interface SearchFilters {
  [key: string]: {
    label: string;
    options: string[];
  };
}

export interface ActiveSearchFilters {
  [key: string]: {
    label: string;
    options: Record<string, boolean>;
  };
}

export interface SearchBarProps {
  filters: SearchFilters;
  onSubmit?: () => void;
}

export const SearchBar = ({ filters, onSubmit }: SearchBarProps) => {
  const [activeFilters, setActiveFilters] = useState<ActiveSearchFilters>(() =>
    Object.fromEntries(
      Object.entries(filters).map(([key, { label, options }]) => {
        return [key, { label, options: Object.fromEntries(options.map((option) => [option, false])) }];
      })
    )
  );

  const handleFilterChange = (filter: string, option: string, isActive: boolean) => {
    return;
    // console.log({ ...activeFilters, ...activeFilters[filter] });
    //setActiveFilters((prevState) => ({ ...prevState, [filter]: prevState[filter] }));
  };

  return (
    <div className="searchbar d-flex">
      <div className="container-fluid">
        <div className="row">
          <div className="col-md-auto p-0">
            <div className="dropdown d-flex p-2 w-100 justify-content-center justify-content-lg-start justify-content-xl-start flex-wrap">
              <span className="text-nowrap m-2">Filter By:</span>
              <div className="d-flex">
                {Object.entries(activeFilters).map(([key, filter]) => {
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
                          <div className="dropdown-item" key={name}>
                            <div className="form-check">
                              <input
                                checked={active}
                                className="form-check-input"
                                name={key}
                                value={name}
                                type="checkbox"
                                id={key + name + 'checkbox'}
                                onChange={() => handleFilterChange(key, name, !active)}
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
              <form className="input-group m-2" method="get" role="form" onSubmit={onSubmit}>
                <input required name="search_term" type="text" className="form-control" placeholder="Search" />
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
