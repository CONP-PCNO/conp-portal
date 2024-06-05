import React, { useEffect, useState } from 'react';

import { Dropdowns } from './Dropdowns';
import { SearchBar } from './SearchBar';

import { type Experiment } from '@/features/experiments/types';
import { ExperimentCard } from '@/features/experiments/components/ExperimentCard';
import { ExperimentTableContext, SearchFilters } from '../../context/ExperimentTableContext';
import { PaginationNav } from './PaginationNav';

const sortKeyOptions = {
  titleAsc: {
    label: 'Title (Ascending)',
    key: 'title',
    method: 'ascending'
  },
  titleDesc: {
    label: 'Title (Descending)',
    key: 'title',
    method: 'descending'
  }
} as const;

type SortKeyOptions = keyof typeof sortKeyOptions;

interface ExperimentTableProps {
  experiments: Experiment[];
  keyword: string;
}

export const ExperimentTable = ({ experiments: initialExperiments , keyword: keywordSearch}: ExperimentTableProps) => {
  const [activeSortKey, setActiveSortKey] = useState<SortKeyOptions>('titleAsc');
  const [currentPage, setCurrentPage] = useState(0);
  const [itemsPerPage, setItemsPerPage] = useState(10);
  const [filteredExperiments, setFilteredExperiments] = useState<Experiment[]>(initialExperiments);
  const [searchT, setSearchT] = useState<string>(keywordSearch || '');

  // by default, all filters are set to false
  const [searchFilters, setSearchFilters] = useState<SearchFilters>(() => {
    const filters = {
      modalities: {
        label: 'Modalities',
        options: Array.from(new Set(initialExperiments.flatMap((item) => item.modalities)))
      },
      primaryFunction: {
        label: 'Primary Function',
        options: Array.from(new Set(initialExperiments.flatMap((item) => item.primaryFunction)))
      },
      primarySoftware: {
        label: 'Primary Software',
        options: Array.from(new Set(initialExperiments.flatMap((item) => item.primarySoftware)))
      }
    };
    return Object.fromEntries(
      Object.entries(filters).map(([key, { label, options }]) => {
        return [key, { label, options: Object.fromEntries(options.map((option) => [option, false])) }];
      })
    );
  });

  // Fonction pour effectuer la recherche
  const performSearch = (term) => {
    const lowerCaseTerm = term.toLowerCase();
    const results = initialExperiments.filter(exp => 
      exp.title.toLowerCase().includes(lowerCaseTerm) ||
      (exp.creators && exp.creators.some(creator => typeof creator === 'string' && creator.toLowerCase().includes(lowerCaseTerm))) ||
      (exp.dateAdded && exp.dateAdded.toString().toLowerCase().includes(lowerCaseTerm)) ||
      (exp.dateUpdated && exp.dateUpdated.toString().toLowerCase().includes(lowerCaseTerm)) ||
      (exp.modalities && exp.modalities.some(modality => typeof modality === 'string' && modality.toLowerCase().includes(lowerCaseTerm))) ||
      (exp.license && typeof exp.license === 'string' && exp.license.toLowerCase().includes(lowerCaseTerm)) ||
      (exp.primaryFunction && typeof exp.primaryFunction === 'string' && exp.primaryFunction.toLowerCase().includes(lowerCaseTerm))||
      (exp.keywords && exp.keywords.includes(lowerCaseTerm))
    );
    setFilteredExperiments(results);
  };

  const anyFilterActive = () =>
    Object.values(searchFilters)
      .map(({ options }) => Object.values(options))
      .flat()
      .includes(true);

  // when search filters change, experiments will be mutated
  useEffect(() => {
    setFilteredExperiments(initialExperiments);
    return;
  }, [searchFilters]);

  // Effectuer une recherche initiale avec keywordSearch si disponible
  useEffect(() => {
    if (keywordSearch && keywordSearch.trim() !== '') {
      performSearch(keywordSearch);
    }
  }, [keywordSearch]); // Dépendance : keywordSearch

  // const filterExperiments = (experimentsList: Experiment[]) => {
  //   if (anyFilterActive()) {
  //     return experimentsList.filter((experiment) => {
  //       // Vérifier chaque catégorie de filtre
  //       for (const category in searchFilters) {
  //         // Vérifier chaque option dans la catégorie
  //         for (const [option, isActive] of Object.entries(searchFilters[category].options)) {
  //           if (isActive) {
  //             const value = experiment[category as keyof Experiment];
  //             if (typeof value === 'string') {
  //               // Si la valeur n'est pas égale à l'option active, exclure l'expérience
  //               if (option !== value) {
  //                 return false;
  //               }
  //             } else if (value instanceof Array) {
  //               // Si l'option active n'est pas incluse dans la valeur, exclure l'expérience
  //               if (!value.includes(option)) {
  //                 return false;
  //               }
  //             }
  //           }
  //         }
  //       }
  //       // Si l'expérience passe tous les filtres, l'inclure dans les résultats
  //       return true;
  //     });
  //   }
  //   return experimentsList;
  // }
  
  const filterExperiments = (experimentsList: Experiment[]) => {
    return experimentsList.filter((experiment) => {
      // Booléen pour vérifier si toutes les catégories de filtres sont validées
      let isCategoryMatch = true;
  
      for (const category in searchFilters) {
        let categoryOptions = searchFilters[category].options;
        let activeOptions = Object.entries(categoryOptions).filter(([_, isActive]) => isActive);
  
        if (activeOptions.length > 0) {
          // Vérifie si au moins une des options actives est satisfaite pour cette catégorie (logique OR)
          let isOptionMatch = activeOptions.some(([option, _]) => {
            let experimentValue = experiment[category];
            if (Array.isArray(experimentValue)) {
              return experimentValue.includes(option);
            } else {
              return option === experimentValue;
            }
          });
  
          // Si aucune option ne correspond dans cette catégorie, définir isCategoryMatch à false
          if (!isOptionMatch) {
            isCategoryMatch = false;
            break;
          }
        }
      }
  
      return isCategoryMatch;
    });
  }
  

  const sortExperiments = (experimentsList: Experiment[]) => {
    const { key, method } = sortKeyOptions[activeSortKey];
    return experimentsList.sort((a, b) => {
      return method === 'ascending' ? (a[key] > b[key] ? 1 : -1) : a[key] < b[key] ? 1 : -1;
    });
  };

  let processedExperiments = filterExperiments(filteredExperiments);
  processedExperiments = sortExperiments(processedExperiments);

  const totalItems = processedExperiments.length;

  const getDownloadLink = (experimentId) => {
    return `/experiments/download/${experimentId}`;
  };

  // Pagination
  const firstItemIndex = currentPage * itemsPerPage;
  const lastItemIndex = Math.min(firstItemIndex + itemsPerPage, processedExperiments.length);
  const displayedExperiments  = processedExperiments.slice(firstItemIndex, lastItemIndex);

  return (
    <ExperimentTableContext.Provider
      value={{
        items: displayedExperiments,
        pagination: {
          currentPage,
          itemsPerPage,
          firstItemIndex,
          lastItemIndex,
          totalItems
        },
        sortKey: {
          active: activeSortKey,
          options: sortKeyOptions
        },
        searchFilters,
        toggleSearchFilter: (category, option, isActive) => {
          setSearchFilters((prevFilters) => {
            const newFilters = { ...prevFilters };
            newFilters[category]['options'][option] = isActive;
            return newFilters;
          });
        },
        setActiveSortKey: (active) => setActiveSortKey(active as SortKeyOptions),
        setCurrentPage: setCurrentPage,
        setItemsPerPage: setItemsPerPage
      }}
    >
        <SearchBar 
        word={searchT}
        onSubmit={(term) => performSearch(term || searchT)} />

      <Dropdowns />
      <div className="search-dataset-table">
        {displayedExperiments.map((experiment) => (
          <ExperimentCard key={experiment.id} experiment={experiment} downloadLink={getDownloadLink(experiment.id)} titleLink={`/experiments/view/${experiment.id}`} />
        ))}
      </div>
      <PaginationNav />
    </ExperimentTableContext.Provider>
  );
};
