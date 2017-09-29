import React from 'react';
import { connect } from 'react-redux';

import Card from './Card';

import * as modalActions from './../actions/modalActions';
import * as cardActions from './../actions/cardActions';
import * as listActions from './../actions/listActions';


const CardList = ({cards, list, onDeleteClick, onEditClick, onMoveCard, isListDragging, onUpdateListCounts, toggleOverlfow, checkScroll, falseScroll}) => {
	console.log(cards)
	console.log('@@@@@@@@@@@@@@@@@@')
	let listCards = cards.filter( c => {
		return c.list === list;
	});
	return (
		<ul className="idea-list__wrapper">
		{
			listCards.map(card => {

				return (
					<Card 
						key={card.id}
						id={card.id}
						onDeleteClick={() => onDeleteClick(card)}
						onEditClick={() => onEditClick(card)}
						onMove={(sourceId, targetId, isDrop) => onMoveCard(sourceId, targetId, isDrop)}
						onUpdateListCounts={(listID, idea_count, want_count, isMove, isDelete) => onUpdateListCounts(listID, idea_count, want_count, isMove, isDelete)}
						isListDragging={isListDragging}
						card={card}
						toggleOverlfow={toggleOverlfow}
						checkScroll={checkScroll}
						falseScroll={falseScroll}
					/>
				);
			})
		}
		</ul>
	);
};

const getCardOrder = (cards, filter) => {

	switch (filter) {
		case 'DISPLAY_WANTOO':
			return cards;
			break;
		case 'DISPLAY_TRELLO':
			return cards;
			break;
		default:
			return cards;
			break;
	}

};

const mapStateToCardListProps = (state, containerProps) => {
	return {
		cards: getCardOrder(state.cards, state.displayFilter),
		list: containerProps.list,
		isListDragging: containerProps.isListDragging
	};
};

const mapDispacheToCardListProps = (dispatch) => {
	return {
		onDeleteClick: (card) =>  {
			console.log('Card Actions => ', cardActions);
			dispatch( modalActions.showModal('DELETE_CARD', card.id, false, card) )
		},
		onEditClick: (card) => {
			window.Intercom("trackEvent", " Edit idea");
			dispatch( modalActions.showModal('UPDATE_CARD', card.id, true, card) );
		},
		onMoveCard: (sourceId, targetId, isDrop) => {
			dispatch( cardActions.moveCard(sourceId, targetId, isDrop) );
		},
		onUpdateListCounts: (listID, idea_count, want_count, isMove, isDelete) => {
			dispatch( listActions.updateListCounts(listID, idea_count, want_count, isMove, isDelete) )
		}
	};
};

const OrderedCards = connect(mapStateToCardListProps, mapDispacheToCardListProps)(CardList);

export default OrderedCards;